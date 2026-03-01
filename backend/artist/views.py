from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import (
    ArtistSerializer,
    ArtistSimpleSerializer,
    AlbumArtistSerializer,
    RelatedArtistSerializer
)
from .models import Artist


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
