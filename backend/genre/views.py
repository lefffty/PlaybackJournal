from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


from .serializers import GenreSerializer, GenreSimpleSerializer
from .models import Genre
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
        if self.action in ('retrieve'):
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
