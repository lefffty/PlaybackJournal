from rest_framework import serializers
from django.db.models import Model

from .models import Genre


class GenreSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
        )


class GenreSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()
    artists = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'description',
            'albums',
            'artists',
        )

    def get_albums(self, obj: Model):
        from albums.serializers import AlbumGenreSerializer
        albums = obj.albums.all()[:5]
        serializer = AlbumGenreSerializer(
            albums,
            many=True,
            read_only=True)
        return serializer.data

    def get_artists(self, obj: Model):
        from artist.serializers import ArtistSimpleSerializer
        artists = obj.artists.all()[:5]
        serializer = ArtistSimpleSerializer(
            artists,
            many=True,
            read_only=True
        )
        return serializer.data


class GenreAlbumCreateSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
    )

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        return {
            'genre': ret['id']
        }
