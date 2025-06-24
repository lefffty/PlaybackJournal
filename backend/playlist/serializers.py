from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.db.transaction import atomic

from .models import (
    Playlist,
    PlaylistSong
)
from song.serializers import (
    SongSerializer,
    SongSimpleSerializer
)
from users.serializers import UserSimpleSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    playlist_id = serializers.IntegerField(source='id')
    playlist_name = serializers.CharField(source='name')
    playlist_description = serializers.CharField(source='description')
    playlist_cover = serializers.ImageField(source='cover')
    playlist_songs = SongSerializer(read_only=True, many=True, source='songs')
    playlist_author = UserSimpleSerializer(read_only=True, source='author')

    class Meta:
        model = Playlist
        fields = (
            'playlist_id',
            'playlist_author',
            'playlist_name',
            'playlist_description',
            'playlist_cover',
            'playlist_songs',
        )


class PlaylistCreateUpdateSerializer(serializers.ModelSerializer):
    songs = SongSimpleSerializer(many=True)
    cover = Base64ImageField()

    class Meta:
        model = Playlist
        fields = (
            'id',
            'name',
            'description',
            'songs',
            'cover',
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
            'cover': {
                'required': True,
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            self.fields['cover'].required = False

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

    @atomic
    def create(self, validated_data):
        songs = validated_data.pop('songs')
        playlist = Playlist.objects.create(
            **validated_data,
        )
        self._save_songs(playlist, songs)
        return playlist

    @atomic
    def update(self, instance, validated_data):
        songs = validated_data.pop('songs', None)
        super().update(instance, validated_data)
        self._save_songs(instance, songs)
        instance.save()
        return instance

    def to_representation(self, instance):
        return PlaylistSerializer(instance).data
