from rest_framework import serializers

from .models import Playlist
from song.serializers import SongSerializer
from users.serializers import UserSimpleSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(read_only=True, many=True)
    author = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Playlist
        fields = (
            'author',
            'name',
            'description',
            'songs',
        )


class PlaylistCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = (
            'name',
            'description',
            'songs',
        )
