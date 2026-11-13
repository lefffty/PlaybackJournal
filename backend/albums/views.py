from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)

from django.db.models import Model
from django.http import HttpRequest

from review.serializers import ReviewListSerializer
from albums.constants import RatedAlbumConsts
from .serializers import (
    AlbumCreateSerializer,
    AlbumSerializer,
)
from .models import (
    FavouriteAlbum,
    ListenedAlbum,
    WishlistAlbum,
    RatedAlbum,
    Album,
)


class AlbumListDetailViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Album.objects.all()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = Album.objects.all()
        if self.action in ("list", "retrieve"):
            qs = qs.prefetch_related("artists", "genres", "songs")
        return qs

    def get_serializer_class(self):
        if self.action in ('create',):
            return AlbumCreateSerializer
        return AlbumSerializer

    def get_permissions(self):
        protected_actions = ('create', 'status', 'favourite', 'rated', 'listened', 'wishlist')
        if self.action in protected_actions:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(
        detail=True,
        methods=['GET'],
        url_path='reviews',
    )
    def reviews(self, request: HttpRequest, pk: int):
        album = self.get_object()
        reviews = album.reviews.all().select_related("author")
        serializer = ReviewListSerializer(reviews,many=True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['GET'],
        url_path='statistics',
    )
    def statistics(self, request: HttpRequest, pk: int):
        album = self.get_object()
        return Response(album.reviews_statistics, status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_path='status',
    )
    def status(self, request: HttpRequest, pk):
        user = request.user
        album = self.get_object()

        filter_kwargs = {
            'user': user,
            'album': album,
        }

        rating = RatedAlbum.objects.filter(**filter_kwargs).values_list('rating', flat=True).first()

        data = {
            'listened': ListenedAlbum.objects.filter(**filter_kwargs).exists(),
            'favourite': FavouriteAlbum.objects.filter(**filter_kwargs).exists(),
            'rating': rating or 0,
            'wishlist': WishlistAlbum.objects.filter(**filter_kwargs).exists(),
        }

        return Response(data, status=status.HTTP_200_OK)

    def _set_rating(self, request: HttpRequest, pk: int):
        album = self.get_object()
        user = request.user

        params = {
            'user': user,
            'album': album,
        }

        try:
            rating = int(request.data.get('rating'))
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Некорректный формат оценки'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (RatedAlbumConsts.MIN_RATING <= rating <= RatedAlbumConsts.MAX_RATING):
            return Response(
                {
                    'detail': 'Оценка должна быть в диапазоне от {} до {}'.format(
                        RatedAlbumConsts.MIN_RATING,
                        RatedAlbumConsts.MAX_RATING,
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = RatedAlbum.objects.filter(**params)

        if instance.exists():
            old_rating = instance[0].rating
            if old_rating == rating:
                instance.delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            instance[0].rating = rating
            instance[0].save(update_fields=['rating'])
            return Response(
                {"rating": rating},
                status=status.HTTP_200_OK
            )
        params['rating'] = rating
        RatedAlbum.objects.create(**params)
        return Response(status=status.HTTP_201_CREATED)

    def _toggle_album_item(self, request: HttpRequest, _Model: Model):
        album = self.get_object()
        user = request.user
        params = {"album": album, "user": user}
        instance = _Model.objects.filter(**params)
        if instance.exists():
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        _Model.objects.create(**params)
        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST'],
        url_path='favourite'
    )
    def favourite(self, request, pk):
        return self._toggle_album_item(request, FavouriteAlbum)

    @action(
        detail=True,
        methods=['POST'],
        url_path='listened'
    )
    def listened(self, request, pk):
        return self._toggle_album_item(request, ListenedAlbum)

    @action(
        detail=True,
        methods=['POST'],
        url_path='wishlist'
    )
    def wishlist(self, request, pk):
        return self._toggle_album_item(request, WishlistAlbum)

    @action(
        detail=True,
        methods=['POST'],
        url_path='rated'
    )
    def rated(self, request: HttpRequest, pk):
        return self._set_rating(request, pk)
