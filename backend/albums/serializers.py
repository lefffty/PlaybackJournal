from rest_framework import serializers
from statistics import mean
from typing import MutableMapping
from drf_extra_fields.fields import Base64ImageField
from django.db.transaction import atomic
from django.db.models import Count

from .models import (
    AlbumArtist,
    AlbumGenre,
    RatedAlbum,
    AlbumSong,
    Album,
    Song,
)
from artist.serializers import (
    ArtistAlbumCreateSerializer,
    ArtistSimpleSerializer,
)
from review.serializers import (
    ReviewListSerializer
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
    artists = ArtistSimpleSerializer(
        read_only=True,
        many=True,
    )
    genres = GenreSimpleSerializer(
        read_only=True,
        many=True,
    )
    songs = SongSerializer(read_only=True, many=True)
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewListSerializer(many=True, read_only=True)
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = (
            'id',
            'name',
            'publication_date',
            'average_rating',
            'cover',
            'songs',
            'reviews',
            'statistics',
            'artists',
            'genres',
        )

    def get_statistics(self, obj: Album):
        entries = obj.reviews.values('type').annotate(total=Count('id'))
        stats = {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
        }
        for entry in entries:
            stats[entry['type']] = entry['total']
        stats['total'] = obj.reviews.count()
        return stats

    def get_average_rating(self, obj: Album):
        instances = RatedAlbum.objects.filter(album=obj)
        if not instances.exists():
            return '-'
        ratings = list(map(lambda instance: instance.rating, instances))
        return mean(ratings)


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
