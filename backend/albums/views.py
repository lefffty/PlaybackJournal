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
        if self.action in ('create'):
            return AlbumCreateSerializer
        return AlbumSerializer

    def get_permissions(self):
        if self.action in ('create'):
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(
        detail=True,
        methods=['GET'],
        url_path='album_reviews'
    )
    def get_album_reviews(self, request: HttpRequest, pk: int):
        album = get_object_or_404(Album, pk=pk)
        reviews = album.reviews.all()
        serializer = ReviewListSerializer(reviews, many=True, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['GET'],
        url_path='album_reviews_statistics'
    )
    def get_album_statistics(self, request: HttpRequest, pk: int):
        album = get_object_or_404(Album, pk=pk)
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

    @action(
        detail=True,
        url_path='user_album',
    )
    def user_album(self, request: HttpRequest, pk):
        user = request.user
        album = get_object_or_404(Album, pk=pk)
        data = {
            'listened': False,
            'favourite': False,
            'rating': 0,
            'wishlist': False,
        }
        filter_kwargs = {
            'user': user,
            'album': album,
        }
        if WishlistAlbum.objects.filter(**filter_kwargs).exists():
            data['wishlist'] = True
        if ListenedAlbum.objects.filter(**filter_kwargs).exists():
            data['listened'] = True
        if FavouriteAlbum.objects.filter(**filter_kwargs).exists():
            data['favourite'] = True
        if RatedAlbum.objects.filter(**filter_kwargs).exists():
            instance = RatedAlbum.objects.get(**filter_kwargs)
            data['rating'] = instance.rating
        return Response(data, status=status.HTTP_200_OK)


class UserAlbumsPreferencesViewSet(
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    def _create_user_album_item(self, request: HttpRequest, pk, model: Model):
        album = get_object_or_404(Album, pk=pk)
        user = request.user

        params = {
            'user': user,
            'album': album,
        }

        instance = model.objects.filter(user=user, album=album)
        if model == RatedAlbum:
            rating = request.data.get('rating')
            if instance.exists():
                if rating is None:
                    return Response(
                        {'detail': 'Необходимо указать оценку.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if rating == 0:
                    instance.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                if not (0 < rating <= 10):
                    return Response(
                        {
                            'detail': 'Оценка должна быть в диапазоне от 0 до 10'
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                instance.update(rating=rating)
                return Response(
                    status=status.HTTP_204_NO_CONTENT
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
    def favourite_album(self, request, pk):
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
    def listened_album(self, request, pk):
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
    def wishlist_album(self, request, pk):
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
    def rated_album(self, request: HttpRequest, pk):
        return self._create_user_album_item(
            request,
            pk,
            RatedAlbum,
        )
