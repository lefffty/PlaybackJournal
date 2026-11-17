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


class ArtistDiscography(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'id',
            'username',
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
    artists = ArtistDiscography(many=True, read_only=True)

    class Meta:
        model = Album
        fields = (
            'id',
            'artists',
            'publication_date',
            'cover',
            'name',
        )


class ArtistSerializer(serializers.ModelSerializer):
    albums = serializers.ReadOnlyField(source='earliest_albums')
    similar = serializers.ReadOnlyField()
    genres = GenreSimpleSerializer(
        many=True,
        read_only=True,
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
