from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest

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
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return ArtistSerializer
        return ArtistSimpleSerializer

    @action(
        detail=True,
        url_path='discography'
    )
    def discography(self, request, pk: int):
        artist = self.get_object()
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
        artist = self.get_object()
        similar = artist.similar_artists.all()
        serializer = RelatedArtistSerializer(
            similar,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['GET', 'POST', 'DELETE'],
        url_path='favourite',
        permission_classes=[IsAuthenticated]
    )
    def favourite(self, request: HttpRequest, pk: int):
        user = request.user
        artist = self.get_object()

        fav_qs = FavouriteArtist.objects.filter(user=user, artist=artist)

        if request.method == 'GET':
            return Response({"favourite": fav_qs.exists()}, status=status.HTTP_200_OK)

        if request.method == 'POST':
            FavouriteArtist.objects.get_or_create(user=user, artist=artist)
            return Response({"favourite": True}, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            fav_qs.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
