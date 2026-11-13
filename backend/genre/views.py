from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.http import HttpRequest

from .serializers import GenreSerializer, GenreSimpleSerializer
from .models import Genre, FavouriteGenre
from albums.serializers import AlbumGenreSerializer
from artist.serializers import ArtistSimpleSerializer


class GenreViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = Genre.objects.all()

        if self.action in ("retrieve",):
            qs = qs.prefetch_related("albums", "artists")

        return qs

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return GenreSerializer
        return GenreSimpleSerializer

    @action(
        detail=True,
        methods=['GET'],
        url_path='artists'
    )
    def artists(self, request, pk: int):
        genre = self.get_object()
        artists = genre.artists.all()
        page = self.paginate_queryset(artists)
        serializer = ArtistSimpleSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['GET'],
        url_path='albums',
    )
    def albums(self, request, pk: int):
        genre = self.get_object()
        albums = genre.albums.all().prefetch_related("artists")
        page = self.paginate_queryset(albums)
        serializer = AlbumGenreSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['GET', 'DELETE', 'POST'],
        url_path='favourite',
        permission_classes=[IsAuthenticated]
    )
    def favourite(self, request: HttpRequest, pk: int):
        genre = self.get_object()
        user = request.user

        filter_kwargs = {
            "genre": genre,
            "user": user
        }

        favourite_qs = FavouriteGenre.objects.filter(**filter_kwargs)

        if request.method == 'GET':
            return Response(
                {"favourite": favourite_qs.exists()},
                status=status.HTTP_200_OK
            )

        if request.method == 'DELETE':
            favourite_qs.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        if request.method == 'POST':
            _, created = FavouriteGenre.objects.get_or_create(**filter_kwargs)
            return Response(
                {"favourite": True},
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
