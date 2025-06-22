from rest_framework import serializers

from .models import Artist, RelatedArtists


class ArtistSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'id',
            'username',
            'avatar'
        )


class RelatedArtistSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='related_artist.id')
    username = serializers.CharField(source='related_artist.username')
    avatar = serializers.ImageField(source='related_artist.avatar')

    class Meta:
        model = RelatedArtists
        fields = (
            'id',
            'username',
            'avatar',
        )


class ArtistSerializer(serializers.ModelSerializer):
    albums = serializers.StringRelatedField(
        many=True,
    )
    genres = serializers.StringRelatedField(
        many=True,
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
