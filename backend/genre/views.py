from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.db.models import Model


from .serializers import GenreSerializer, GenreSimpleSerializer
from .models import Genre, FavouriteGenre
from albums.serializers import AlbumGenreSerializer
from artist.serializers import ArtistSimpleSerializer


class GenreListDetailViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = Genre.objects.all()
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return GenreSerializer
        return GenreSimpleSerializer


class GenreListsViewSet(
    viewsets.GenericViewSet
):
    @action(
        detail=True,
        methods=['GET'],
        url_path='artists'
    )
    def get_genre_artists(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)
        artists = genre.artists.all()
        serializer = ArtistSimpleSerializer(artists, many=True, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['GET'],
        url_path='albums'
    )
    def get_genre_albums(self, request, pk: int):
        genre = get_object_or_404(Genre, pk=pk)
        albums = genre.albums.all()
        serializer = AlbumGenreSerializer(albums, many=True, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGenreViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=['GET'],
        url_path='user_genre'
    )
    def user_genre(self, request: HttpRequest, pk: int):
        user = request.user
        genre = get_object_or_404(Genre, pk=pk)

        filter_kwargs = {
            'user': user,
            'genre': genre,
        }

        data = {
            'favourite': False,
        }

        if FavouriteGenre.objects.filter(**filter_kwargs).exists():
            data['favourite'] = True

        return Response(data, status=status.HTTP_200_OK)


class UserGenrePreferencesViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    def _create_user_genre_item(self, request: HttpRequest, pk: int, model: Model):
        user = request.user
        genre = get_object_or_404(Genre, pk=pk)

        filter_kwargs = {
            'user': user,
            'genre': genre,
        }

        instance = model.objects.filter(**filter_kwargs)

        if instance.exists():
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            model.objects.create(**filter_kwargs)
            return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST'],
        url_path='favourite'
    )
    def favourite_genre(self, request: HttpRequest, pk: int):
        return self._create_user_genre_item(
            request,
            pk,
            FavouriteGenre
        )
