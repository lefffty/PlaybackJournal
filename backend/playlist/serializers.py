from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import (
    Playlist,
    PlaylistSong
)
from song.serializers import SongSerializer, SongSimpleSerializer
from song.models import Song
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
    songs = SongSimpleSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Playlist
        fields = (
            'name',
            'description',
            'songs',
            'image',
        )
        extra_kwargs = {
            'name': {
                'required': True,
            },
            'description': {
                'required': False,
            },
            'songs': {
                'required': True,
            },
            'image': {
                'required': True,
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            self.fields['image'].required = False

    def validate_songs(self, value):
        if not value:
            raise serializers.ValidationError(
                detail='Нужно добавить хотя бы одну песню!'
            )
        return value

    def _save_songs(self, playlist, _songs):
        PlaylistSong.objects.filter(
            playlist=playlist
        ).delete()

        songs = []

        for song in _songs:
            songs.append(
                PlaylistSong(
                    playlist=playlist,
                    song=song['song'],
                )
            )

        PlaylistSong.objects.bulk_create(
            songs
        )

    def create(self, validated_data):
        print(validated_data)
        songs = validated_data.pop('songs')
        playlist = Playlist.objects.create(
            **validated_data,
        )
        self._save_songs(playlist, songs)
        return playlist

    def update(self, instance, validated_data):
        songs = validated_data.pop('songs', None)
        super().update(instance, validated_data)
        self._save_songs(instance, songs)
        instance.save()
        return instance
