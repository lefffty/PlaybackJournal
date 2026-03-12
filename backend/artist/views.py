from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .serializers import (
    ArtistSerializer,
    ArtistSimpleSerializer,
    AlbumArtistSerializer,
    RelatedArtistSerializer
)
from .models import (
    Artist,
    FavouriteArtist
)


class ArtistViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = Artist.objects.all()
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('retrieve'):
            return ArtistSerializer
        return ArtistSimpleSerializer


class ArtistDiscographyViewSet(
    viewsets.GenericViewSet,
):
    @action(
        detail=True,
        url_path='discography'
    )
    def discography(self, request, pk: int):
        artist = get_object_or_404(Artist, pk=pk)
        albums = artist.albums.all().order_by('publication_date')
        serializer = AlbumArtistSerializer(
            albums,
            many=True,
            read_only=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_path='similar'
    )
    def similar(self, request, pk: int):
        artist = get_object_or_404(Artist, pk=pk)
        similar = artist.similar_artists.all()
        serializer = RelatedArtistSerializer(
            similar,
            many=True,
            read_only=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserArtistsPreferencesViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    def _create_user_genre_item(self, request: HttpRequest, pk: int, model: Model):
        user = request.user
        artist = get_object_or_404(Artist, pk=pk)

        filter_kwargs = {
            'user': user,
            'artist': artist
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
        url_path='favourite',
    )
    def favourite_genre(self, request: HttpRequest, pk: int):
        return self._create_user_genre_item(
            request,
            pk,
            FavouriteArtist
        )
