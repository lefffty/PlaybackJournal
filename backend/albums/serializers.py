from rest_framework import serializers
from statistics import mean
from typing import MutableMapping
from drf_extra_fields.fields import Base64ImageField
from django.db.transaction import atomic

from .models import (
    AlbumArtist,
    AlbumGenre,
    RatedAlbum,
    AlbumSong,
    Album,
    Song,
)
from .constants import AlbumConsts
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
from review.serializers import (
    ReviewListSerializer
)


class AlbumSerializer(serializers.ModelSerializer):
    artists = ArtistSimpleSerializer(
        read_only=True,
        many=True,
    )
    genres = GenreSimpleSerializer(
        read_only=True,
        many=True,
    )
    songs = SongSerializer(read_only=True, many=True)
    latest_reviews = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Album
        fields = (
            'id',
            'name',
            'publication_date',
            'average_rating',
            'cover',
            'songs',
            'artists',
            'latest_reviews',
            'genres',
        )

    def get_latest_reviews(self, obj: Album):
        reviews = obj.reviews.select_related("author").order_by("-created_at")[:AlbumConsts.REVIEWS_LIMIT]
        return ReviewListSerializer(reviews, many=True, context=self.context).data


class AlbumSimpleSerializer(serializers.ModelSerializer):
    artists = ArtistSimpleSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = (
            'id',
            'name',
            'cover',
            'publication_date',
            'artists',
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
    def create(self, validated_data: MutableMapping):
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


class AlbumGenreSerializer(serializers.ModelSerializer):
    artists = ArtistSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = (
            'id',
            'artists',
            'name',
            'cover',
            'publication_date',
        )
