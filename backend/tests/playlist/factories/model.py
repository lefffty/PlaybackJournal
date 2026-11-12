import factory
from faker import Factory

from playlist.models import Playlist, PlaylistSong, RatedPlaylist, FavouritePlaylist
from playlist.constants import PlaylistsConsts, RatedPlaylistsConsts

from ...song.factories.model import SongFactory
from ...users.factories.model import UserFactory

faker = Factory.create()


class PlaylistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Playlist

    name = factory.LazyFunction(lambda: faker.name()[:PlaylistsConsts.NAME_MAX_LENGTH])
    description = factory.LazyFunction(lambda: faker.sentence()[:PlaylistsConsts.DESCRIPTION_MAX_LENGTH])
    author = factory.SubFactory(UserFactory)
    cover = factory.django.ImageField(
        filename="test_image.jpg", width=200, height=200, color="blue", format="JPEG",
    )

    @factory.post_generation
    def songs(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for song in extracted:
                PlaylistSongFactory(
                    playlist=self,
                    song=song,
                )


class PlaylistSongFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaylistSong

    playlist = factory.SubFactory(PlaylistFactory)
    song = factory.SubFactory(SongFactory)


class FavouritePlaylistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavouritePlaylist

    user = factory.SubFactory(UserFactory)
    playlist = factory.SubFactory(PlaylistFactory)


class RatedPlaylistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RatedPlaylist

    user = factory.SubFactory(UserFactory)
    playlist = factory.SubFactory(PlaylistFactory)
    rating = factory.LazyFunction(
        lambda: faker.pyint(
            min_value=RatedPlaylistsConsts.MIN_RATING,
            max_value=RatedPlaylistsConsts.MAX_RATING,
        )
    )
