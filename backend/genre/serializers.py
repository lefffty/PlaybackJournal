from rest_framework import serializers

from .models import Genre


class GenreSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
        )


class GenreSerializer(serializers.ModelSerializer):
    albums = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    artists = serializers.StringRelatedField(
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


class GenreAlbumCreateSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
    )

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        return {
            'genre': ret['id']
        }
