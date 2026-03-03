from rest_framework import (
    viewsets,
    mixins,
    status
)
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.db.models import Model, Q

from .serializers import (
    UserCreateSerializer,
    UserProfileSerializer,
    AvatarSerializer,
    NewPasswordSerializer,
    UserRatedAlbumsSerializer,
    UserListenedAlbumsSerializer,
    UserFavouriteAlbumsSerialzer,
)

from albums.serializers import AlbumGenreSerializer
from playlist.serializers import PlaylistSimpleSerializer
from artist.serializers import ArtistSimpleSerializer
from song.serializers import SongSerializer

from albums.models import (
    FavouriteAlbum,
    ListenedAlbum,
    RatedAlbum,
)

from artist.models import Artist
from albums.models import Album
from playlist.models import Playlist
from song.models import Song

User = get_user_model()


class UserCreateViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class UserProfileViewSet(
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path='me')
    def profile(self, request):
        """
        """
        serializer = UserProfileSerializer(
            request.user
        )
        return Response(serializer.data)


class AvatarViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['PUT', 'DELETE'], url_path='me/avatar')
    def avatar(self, request: HttpRequest):
        if request.method == 'PUT':
            serializer = AvatarSerializer(
                request.user,
                data=request.data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={
                    'avatar': serializer.data['avatar'],
                }
            )
        request.user.avatar.delete(save=True)
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class NewPasswordViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='set_password')
    def set_password(self, request):
        serializer = NewPasswordSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class SearchViewSet(
    viewsets.GenericViewSet
):
    pagination_class = None

    @action(
        detail=False,
        methods=['GET'],
    )
    def search(self, request: HttpRequest):
        query = request.GET.get('query')
        if not query:
            return Response(
                data='Empty query',
                status=status.HTTP_204_NO_CONTENT
            )
        albums = Album.objects.filter(Q(name__icontains=query))
        playlists = Playlist.objects.filter(Q(name__icontains=query))
        songs = Song.objects.filter(Q(name__icontains=query))
        artists = Artist.objects.filter(Q(username__icontains=query))
        albums_serialized = AlbumGenreSerializer(
            albums, many=True, read_only=True).data
        playlists_serialized = PlaylistSimpleSerializer(
            playlists, many=True, read_only=True).data
        songs_serialized = SongSerializer(
            songs, many=True, read_only=True).data
        artists_serialized = ArtistSimpleSerializer(
            artists, many=True, read_only=True).data
        return Response(
            data={
                'albums': albums_serialized,
                'playlists': playlists_serialized,
                'songs': songs_serialized,
                'artists': artists_serialized,
            },
            status=status.HTTP_200_OK
        )


class UserAlbumsListsViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    def _get_albums_list(
        self,
        request: HttpRequest,
        model: Model,
        serializer: serializers.ModelSerializer
    ):
        user = request.user
        objects = model.objects.filter(
            user=user,
        )
        _serializer = serializer(objects, many=True)
        return Response(
            _serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['GET'], url_path='favorite/albums')
    def favourite(self, request):
        return self._get_albums_list(
            request,
            FavouriteAlbum,
            UserFavouriteAlbumsSerialzer,
        )

    @action(detail=False, methods=['GET'], url_path='listened/albums')
    def listened(self, request):
        return self._get_albums_list(
            request,
            ListenedAlbum,
            UserListenedAlbumsSerializer,
        )

    @action(detail=False, methods=['GET'], url_path='rated/albums')
    def rated(self, request):
        return self._get_albums_list(
            request,
            RatedAlbum,
            UserRatedAlbumsSerializer,
        )
