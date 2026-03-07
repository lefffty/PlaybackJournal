from rest_framework import serializers

from .models import Song
from artist.serializers import ArtistAlbumCreateSerializer


class SongListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = (
            'id',
            'name',
        )


class SongSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = (
            'id',
            'name',
            'duration',
            'cover',
            'album',
        )

    def get_album(self, obj):
        from albums.serializers import AlbumGenreSerializer
        if obj.albumsong_set.first():
            album = obj.albumsong_set.first().album
            serializer = AlbumGenreSerializer(album)
            return serializer.data
        return None

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
