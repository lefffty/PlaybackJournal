from rest_framework import serializers

from .models import Song
from artist.serializers import ArtistAlbumCreateSerializer


class SongListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = (
            'id',
            'name',
            'cover',
        )


class SongSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = (
            'id',
            'name',
            'duration',
            'cover',
        )

    def get_cover(self, obj):
        request = self.context.get('request')
        instance = obj.albumsong_set.first()
        if instance:
            cover = instance.album.cover
            if request:
                return request.build_absolute_uri(cover.url)
            return cover.url
        return r'http://localhost:8000/media/default_images/default%20song%20cover.jpg'


class SongSimpleSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all()
    )

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        return {
            'song': ret['id']
        }


class SongAlbumCreateSerializer(serializers.ModelSerializer):
    artists = ArtistAlbumCreateSerializer(many=True, required=False)

    class Meta:
        model = Song
        fields = (
            'name',
            'duration',
            'artists',
        )
