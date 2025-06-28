from rest_framework import serializers
from typing import Dict
from drf_extra_fields.fields import Base64ImageField
from django.db.transaction import atomic

from .models import (
    AlbumArtist,
    AlbumGenre,
    AlbumSong,
    Artist,
    Album,
    Genre,
    Song,
)
from artist.serializers import (
    ArtistAlbumCreateSerializer,
    ArtistSimpleSerializer,
)
from genre.serializers import (
    GenreAlbumCreateSerializer,
    GenreSimpleSerializer,
)
from song.serializers import (
    SongAlbumCreateSerializer,
    SongSerializer,
)


class AlbumSerializer(serializers.ModelSerializer):
    album_id = serializers.IntegerField(source='id')
    album_artists = ArtistSimpleSerializer(
        read_only=True,
        many=True,
        source='artists',
    )
    album_genres = GenreSimpleSerializer(
        read_only=True,
        many=True,
        source='genres',
    )
    album_songs = SongSerializer(
        read_only=True,
        many=True,
        source='songs',
    )
    album_name = serializers.CharField(source='name')
    album_publication_date = serializers.DateField(source='publication_date')
    album_cover = serializers.ImageField(source='cover')

    class Meta:
        model = Album
        fields = (
            'album_id',
            'album_name',
            'album_publication_date',
            'album_cover',
            'album_artists',
            'album_genres',
            'album_songs',
        )


class AlbumSimpleSerializer(serializers.ModelSerializer):
    album_id = serializers.IntegerField(source='id')
    album_name = serializers.CharField(source='name')
    album_publication_date = serializers.DateField(source='publication_date')
    album_artists = ArtistSimpleSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = (
            'album_id',
            'album_name',
            'album_publication_date',
            'album_artists',
        )


class AlbumCreateSerializer(serializers.ModelSerializer):
    artists = ArtistAlbumCreateSerializer(many=True, required=True)
    genres = GenreAlbumCreateSerializer(many=True, required=True)
    songs = SongAlbumCreateSerializer(many=True, required=True)
    cover = Base64ImageField()

    class Meta:
        model = Album
        fields = (
            'name',
            'publication_date',
            'cover',
            'artists',
            'genres',
            'songs',
        )
        extra_kwargs = {
            'cover': {
                'required': False,
            }
        }

    @atomic
    def create(self, validated_data: Dict):
        songs = validated_data.pop('songs')
        genres = validated_data.pop('genres')
        artists = validated_data.pop('artists')

        album = Album.objects.create(**validated_data)

        for song in songs:
            current_song = Song.objects.create(**song)
            AlbumSong.objects.create(
                song=current_song,
                album=album,
            )

        for genre in genres:
            AlbumGenre.objects.create(
                genre=genre['genre'],
                album=album
            )

        for artist in artists:
            AlbumArtist.objects.create(
                artist=artist['artist'],
                album=album,
            )

        return album

    def to_representation(self, instance):
        return AlbumSerializer(instance).data
