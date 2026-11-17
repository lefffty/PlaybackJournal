from rest_framework import serializers

from .models import Genre


class GenreSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'description',
            'name',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'description',
            'albums',
            'artists',
        )

    def get_fields(self):
        fields = super().get_fields()

        from albums.serializers import AlbumGenreSerializer
        from artist.serializers import ArtistSimpleSerializer

        fields['albums'] = AlbumGenreSerializer(
            many=True, read_only=True, source='limited_albums'
        )
        fields["artists"] = ArtistSimpleSerializer(
            many=True, read_only=True, source='limited_artists'
        )

        return fields


class GenreAlbumCreateSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
    )

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        return {
            'genre': ret['id']
        }
