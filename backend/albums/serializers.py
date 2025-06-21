from rest_framework import serializers

from .models import (
    Album
)
from artist.serializers import ArtistSimpleSerializer
from genre.serializers import GenreSimpleSerializer
from song.serializers import SongSerializer


class AlbumSerializer(serializers.ModelSerializer):
    artists = ArtistSimpleSerializer(read_only=True, many=True)
    genres = GenreSimpleSerializer(read_only=True, many=True)
    songs = SongSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = (
            'name',
            'publication_date',
            'cover',
            'artists',
            'genres',
            'songs',
        )


class AlbumSimpleSerializer(serializers.ModelSerializer):
    artists = ArtistSimpleSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = (
            'name',
            'publication_date',
            'artists'
        )
