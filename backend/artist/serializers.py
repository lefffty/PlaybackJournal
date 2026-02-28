from rest_framework import serializers

from .models import (
    Artist,
    RelatedArtists
)
from genre.serializers import GenreSimpleSerializer
from albums.models import Album


class ArtistSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'id',
            'username',
            'avatar'
        )


class RelatedArtistSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='related_artist.username')
    avatar = serializers.ImageField(source='related_artist.avatar')
    id = serializers.IntegerField(source='related_artist.id')

    class Meta:
        model = RelatedArtists
        fields = (
            'id',
            'username',
            'avatar',
        )


class AlbumArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = (
            'id',
            'cover',
            'name',
        )


class ArtistSerializer(serializers.ModelSerializer):
    albums = AlbumArtistSerializer(
        many=True,
        read_only=True,
    )
    genres = GenreSimpleSerializer(
        many=True,
        read_only=True,
    )
    similar = RelatedArtistSerializer(
        many=True,
        read_only=True,
        source='similar_artists'
    )

    class Meta:
        model = Artist
        fields = (
            'id',
            'username',
            'description',
            'avatar',
            'albums',
            'genres',
            'similar'
        )


class ArtistAlbumCreateSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(),
    )

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        return {
            'artist': ret['id']
        }
