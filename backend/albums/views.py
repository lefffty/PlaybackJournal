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

from django.db.models import Model, Count
from django.shortcuts import get_object_or_404
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

    def get_serializer_class(self):
        if self.action in ('create',):
            return AlbumCreateSerializer
        return AlbumSerializer

    def get_permissions(self):
        if self.action in ('create',):
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(
        detail=True,
        methods=['GET'],
        url_path='album_reviews'
    )
    def reviews(self, request: HttpRequest, pk: int):
        album = get_object_or_404(Album, pk=pk)
        reviews = album.reviews.all()
        serializer = ReviewListSerializer(
            reviews,
            many=True,
            read_only=True,
            context={
                'request': request
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['GET'],
        url_path='album_reviews_statistics'
    )
    def statistics(self, request: HttpRequest, pk: int):
        album = self.get_object()
        entries = album.reviews.values('type').annotate(total=Count('id'))
        stats = {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
        }
        for entry in entries:
            stats[entry['type']] = entry['total']
        stats['total'] = album.reviews.count()
        return Response(stats, status=status.HTTP_200_OK)


class UserAlbumViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]
    queryset = Album.objects.all()

    @action(
        detail=True,
        url_path='user_album',
    )
    def data(self, request: HttpRequest, pk):
        user = request.user
        album = self.get_object()

        filter_kwargs = {
            'user': user,
            'album': album,
        }

        data = {
            'listened': ListenedAlbum.objects.filter(**filter_kwargs).exists(),
            'favourite': FavouriteAlbum.objects.filter(**filter_kwargs).exists(),
            'rating': 0,
            'wishlist': WishlistAlbum.objects.filter(**filter_kwargs).exists(),
        }

        rated_album = RatedAlbum.objects.filter(**filter_kwargs)

        if rated_album:
            data['rating'] = rated_album[0].rating

        return Response(data, status=status.HTTP_200_OK)


class UserAlbumsPreferencesViewSet(
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Album.objects.all()

    def _create_user_album_item(self, request: HttpRequest, pk, model: Model):
        album = self.get_object()
        user = request.user

        params = {
            'user': user,
            'album': album,
        }

        instance = model.objects.filter(**params)

        if model == RatedAlbum:
            rating = request.data.get('rating')

            if rating is None:
                return Response(
                    {'detail': 'Необходимо указать оценку.'},
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

            if instance.exists():
                old_rating = instance[0].rating
                if old_rating == rating:
                    instance.delete()
                    return Response(
                        status=status.HTTP_204_NO_CONTENT
                    )
                instance.update(rating=rating)
                return Response(
                    status=status.HTTP_200_OK
                )
            params['rating'] = rating
            model.objects.create(**params)
            return Response(status=status.HTTP_201_CREATED)
        else:
            if instance.exists():
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            model.objects.create(**params)
            return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST'],
        url_path='favourite'
    )
    def favourite(self, request, pk):
        return self._create_user_album_item(
            request,
            pk,
            FavouriteAlbum,
        )

    @action(
        detail=True,
        methods=['POST'],
        url_path='listened'
    )
    def listened(self, request, pk):
        return self._create_user_album_item(
            request,
            pk,
            ListenedAlbum,
        )

    @action(
        detail=True,
        methods=['POST'],
        url_path='wishlist'
    )
    def wishlist(self, request, pk):
        return self._create_user_album_item(
            request,
            pk,
            WishlistAlbum,
        )

    @action(
        detail=True,
        methods=['POST'],
        url_path='rated'
    )
    def rated(self, request: HttpRequest, pk):
        return self._create_user_album_item(
            request,
            pk,
            RatedAlbum,
        )
