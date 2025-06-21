from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import HttpRequest

from .serializers import AlbumSerializer
from .models import (
    Album,
    ListenedAlbum,
    RatedAlbum,
    FavouriteAlbum
)


class AlbumListDetailViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class AlbumUserViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    def _create_delete_album_user(self, request: HttpRequest, pk, model):
        album = get_object_or_404(Album, pk=pk)
        user = request.user

        if request.method == 'POST':
            if model.objects.filter(user=user, album=album).exists():
                return Response(
                    {'detail': 'Связь альбом-пользователь уже существует'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            params = {'user': user, 'album': album}
            if model == RatedAlbum:
                rating = request.data.get('rating')
                if rating is None:
                    return Response(
                        {'detail': 'Необходимо указать оценку.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                params['rating'] = rating

            model.objects.create(**params)
            return Response(status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            instance = model.objects.filter(user=user, album=album)
            if not instance.exists():
                return Response(
                    {'detail': 'Связи альбом-пользователь не существует'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            url_path='favourite'
    )
    def favourite_albums(self, request, pk):
        return self._create_delete_album_user(
            request,
            pk,
            FavouriteAlbum,
        )

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            url_path='listened'
    )
    def listened_albums(self, request, pk):
        return self._create_delete_album_user(
            request,
            pk,
            ListenedAlbum,
        )

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            url_path='rated'
    )
    def rated_albums(self, request: HttpRequest, pk):
        return self._create_delete_album_user(
            request,
            pk,
            RatedAlbum,
        )
