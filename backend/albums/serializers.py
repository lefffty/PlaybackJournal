from rest_framework import serializers

from .models import (
    Album
)
from artist.serializers import ArtistSimpleSerializer
from genre.serializers import GenreSimpleSerializer
from song.serializers import SongSerializer


class AlbumSerializer(serializers.ModelSerializer):
    album_id = serializers.IntegerField(source='id')
    album_artists = ArtistSimpleSerializer(
        read_only=True,
        many=True,
        source='artists',
    )
    album_genres = GenreSimpleSerializer(
        read_only=True,
        many=True,
        source='genres',
    )
    album_songs = SongSerializer(
        read_only=True,
        many=True,
        source='songs',
    )
    album_name = serializers.CharField(source='name')
    album_publication_date = serializers.DateField(source='publication_date')
    album_cover = serializers.ImageField(source='cover')

    class Meta:
        model = Album
        fields = (
            'album_id',
            'album_name',
            'album_publication_date',
            'album_cover',
            'album_artists',
            'album_genres',
            'album_songs',
        )


class AlbumSimpleSerializer(serializers.ModelSerializer):
    album_id = serializers.IntegerField(source='id')
    album_name = serializers.CharField(source='name')
    album_publication_date = serializers.DateField(source='publication_date')
    album_artists = ArtistSimpleSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = (
            'album_id',
            'album_name',
            'album_publication_date',
            'album_artists',
        )
