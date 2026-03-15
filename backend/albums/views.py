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
from django.shortcuts import get_object_or_404
from django.http import HttpRequest

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
        response = {
            'listened': False,
            'favourite': False,
            'rating': 0,
        }
        if ListenedAlbum.objects.filter(user=user, album=album).exists():
            response['listened'] = True
        if FavouriteAlbum.objects.filter(user=user, album=album).exists():
            response['favourite'] = True
        if RatedAlbum.objects.filter(user=user, album=album).exists():
            instance = RatedAlbum.objects.get(user=user, album=album)
            response['rating'] = instance.rating
        return Response(response, status=status.HTTP_200_OK)


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
                if not (0 <= rating <= 10):
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
                instance[0].delete()
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
