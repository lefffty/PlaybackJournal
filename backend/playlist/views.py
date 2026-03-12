from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.db.models import Model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .serializers import (
    PlaylistSerializer,
    PlaylistDetailSerializer,
    PlaylistCreateUpdateSerializer
)
from .permissions import OwnerOrReadOnly
from .models import (
    Playlist,
    RatedPlaylist,
    FavouritePlaylist
)


class PlaylistViewSet(
    viewsets.ModelViewSet
):
    queryset = Playlist.objects.all()
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'create'):
            return [IsAuthenticatedOrReadOnly()]
        return [OwnerOrReadOnly()]

    def get_serializer_class(self):
        if self.action in ('list',):
            return PlaylistSerializer
        if self.action in ('retrieve',):
            return PlaylistDetailSerializer
        return PlaylistCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PlaylistCreateUserViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    def _create_delete_playlist_user(
        self,
        request: HttpRequest,
        pk: int,
        model: Model
    ):
        playlist = get_object_or_404(Playlist, pk=pk)
        user = request.user

        params = {
            'playlist': playlist,
            'user': user
        }

        instance = model.objects.filter(user=user, playlist=playlist)
        if model == RatedPlaylist:
            rating = request.data.get('rating')
            if instance.exists():
                if rating is None:
                    return Response(
                        {'detail': ''},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if not (0 <= rating <= 10):
                    return Response(
                        {'detail': ''},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                instance.update(rating=rating)
                return Response(
                    status=status.HTTP_204_NO_CONTENT,
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
    def favourite_playlists(self, request: HttpRequest, pk: int):
        return self._create_delete_playlist_user(
            request,
            pk,
            FavouritePlaylist
        )

    @action(
        detail=True,
        methods=['POST'],
        url_path='rated'
    )
    def rated_playlists(self, request: HttpRequest, pk: int):
        return self._create_delete_playlist_user(
            request,
            pk,
            RatedPlaylist,
        )


class UserPlaylistViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        url_path='user_playlist',
    )
    def user_playlist(self, request: HttpRequest, pk: int):
        playlist = get_object_or_404(Playlist, pk=pk)
        user = request.user

        response = {
            'favourite': False,
            'rating': 0,
        }

        if FavouritePlaylist.objects.filter(user=user, playlist=playlist).exists():
            response['favourite'] = True

        if RatedPlaylist.objects.filter(user=user, playlist=playlist).exists():
            instance = RatedPlaylist.objects.get(user=user, playlist=playlist)
            response['rating'] = instance.rating

        return Response(response, status=status.HTTP_200_OK)
