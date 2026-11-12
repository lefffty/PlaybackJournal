import factory
from faker import Factory
from datetime import datetime

from albums.models import (
    Album,
    AlbumGenre,
    AlbumArtist,
    AlbumSong,
    RatedAlbum,
    FavouriteAlbum,
    ListenedAlbum,
    WishlistAlbum
)
from albums.constants import AlbumConsts, RatedAlbumConsts

from tests.artist.factories.model import ArtistFactory
from tests.song.factories.model import SongFactory
from tests.genre.factories.model import GenreFactory
from tests.users.factories.model import UserFactory

faker = Factory.create()


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album

    name = factory.LazyFunction(lambda: faker.name()[:AlbumConsts.NAME_MAX_LENGTH])
    publication_date = factory.LazyFunction(lambda: datetime.now().date())
    cover = factory.django.ImageField(
        filename="test_image.jpg", width=200, height=200, color="blue", format="JPEG",
    )

    @factory.post_generation
    def songs(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for song in extracted:
                AlbumSongFactory(
                    album=self, song=song, **kwargs
                )

    @factory.post_generation
    def artists(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for artist in extracted:
                AlbumArtistFactory(
                    album=self, artist=artist, **kwargs
                )

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for genre in extracted:
                AlbumGenreFactory(
                    album=self, genre=genre, **kwargs
                )


class AlbumGenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AlbumGenre
        django_get_or_create = ("album", "genre")

    album = factory.SubFactory(AlbumFactory)
    genre = factory.SubFactory(GenreFactory)


class AlbumArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AlbumArtist
        django_get_or_create = ("album", "artist")

    album = factory.SubFactory(AlbumFactory)
    artist = factory.SubFactory(ArtistFactory)


class AlbumSongFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AlbumSong
        django_get_or_create = ("album", "song")

    album = factory.SubFactory(AlbumFactory)
    song = factory.SubFactory(SongFactory)


class RatedAlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RatedAlbum
        django_get_or_create = ("album", "user")

    user = factory.SubFactory(UserFactory)
    album = factory.SubFactory(AlbumFactory)
    rating = factory.LazyFunction(
        lambda: faker.pyint(
            min_value=RatedAlbumConsts.MIN_RATING,
            max_value=RatedAlbumConsts.MAX_RATING,
        )
    )


class FavouriteAlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavouriteAlbum
        django_get_or_create = ("album", "user")

    user = factory.SubFactory(UserFactory)
    album = factory.SubFactory(AlbumFactory)


class ListenedAlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ListenedAlbum
        django_get_or_create = ("album", "user")

    user = factory.SubFactory(UserFactory)
    album = factory.SubFactory(AlbumFactory)


class WishlistAlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishlistAlbum
        django_get_or_create = ("album", "user")

    user = factory.SubFactory(UserFactory)
    album = factory.SubFactory(AlbumFactory)
