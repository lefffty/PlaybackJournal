from rest_framework import serializers

from .models import Genre


class GenreSimpleSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='name')
    genre_id = serializers.IntegerField(source='id')

    class Meta:
        model = Genre
        fields = (
            'genre_id',
            'genre_name',
        )


class GenreSerializer(serializers.ModelSerializer):
    genre_id = serializers.IntegerField(source='id')
    genre_name = serializers.CharField(source='name')
    genre_description = serializers.CharField(source='description')
    genre_albums = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    genre_artists = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'description',
            'albums',
            'artists',
        )
