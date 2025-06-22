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
    similar_artists = serializers.StringRelatedField(
        many=True,
    )

    class Meta:
        model = Artist
        fields = (
            'username',
            'description',
            'avatar',
            'similar_artists'
        )
