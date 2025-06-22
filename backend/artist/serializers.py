from rest_framework import serializers

from .models import Artist


class ArtistSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'username',
            'avatar'
        )


class ArtistSerilizer(serializers.ModelSerializer):
    albums = serializers.StringRelatedField(
        many=True,
    )
    genres = serializers.StringRelatedField(
        many=True,
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
        )
