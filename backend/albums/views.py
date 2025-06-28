from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from django.shortcuts import get_object_or_404
from django.http import HttpRequest

from .serializers import (
    AlbumCreateSerializer,
    AlbumSerializer,
)
from .models import (
    FavouriteAlbum,
    ListenedAlbum,
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
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ('create'):
            return AlbumCreateSerializer
        return AlbumSerializer

    def get_permissions(self):
        if self.action in ('create'):
            return [IsAuthenticated()]
        return [AllowAny()]


class AlbumCreateUserViewSet(
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

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
                if not (0 <= rating <= 10):
                    return Response(
                        {
                            'detail': 'Оценка должна быть в диапазоне от 0 до 10'
                        },
                        status=status.HTTP_400_BAD_REQUEST,
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
