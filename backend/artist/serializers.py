from rest_framework import serializers

from .models import (
    Artist,
    RelatedArtists
)
from genre.serializers import GenreSimpleSerializer
from albums.models import Album


class ArtistSimpleSerializer(serializers.ModelSerializer):
    artist_username = serializers.CharField(source='username')
    artist_avatar = serializers.ImageField(source='avatar')
    artist_id = serializers.IntegerField(source='id')

    class Meta:
        model = Artist
        fields = (
            'artist_id',
            'artist_username',
            'artist_avatar'
        )


class RelatedArtistSerializer(serializers.ModelSerializer):
    artist_id = serializers.IntegerField(source='related_artist.id')
    artist_username = serializers.CharField(source='related_artist.username')
    artist_avatar = serializers.ImageField(source='related_artist.avatar')

    class Meta:
        model = RelatedArtists
        fields = (
            'artist_id',
            'artist_username',
            'artist_avatar',
        )


class AlbumArtistSerializer(serializers.ModelSerializer):
    album_id = serializers.IntegerField(source='id')
    album_name = serializers.CharField(source='name')

    class Meta:
        model = Album
        fields = (
            'album_id',
            'album_name',
        )


class ArtistSerializer(serializers.ModelSerializer):
    artist_id = serializers.IntegerField(source='id')
    artist_username = serializers.CharField(source='username')
    artist_description = serializers.CharField(source='description')
    artist_avatar = serializers.ImageField(source='avatar')
    artist_albums = AlbumArtistSerializer(
        many=True,
        read_only=True,
        source='albums',
    )
    artist_genres = GenreSimpleSerializer(
        many=True,
        read_only=True,
        source='genres',
    )
    artist_similar = RelatedArtistSerializer(
        many=True,
        read_only=True,
        source='similar_artists'
    )

    class Meta:
        model = Artist
        fields = (
            'artist_id',
            'artist_username',
            'artist_description',
            'artist_avatar',
            'artist_albums',
            'artist_genres',
            'artist_similar'
        )
