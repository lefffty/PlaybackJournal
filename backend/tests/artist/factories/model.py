from tests.song.factories.model import SongFactory

import factory
from faker import Factory

from artist.models import Artist, ArtistSong, FavouriteArtist
from artist.constants import ArtistConsts
from tests.users.factories.model import UserFactory

faker = Factory.create()


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Artist

    username = factory.LazyFunction(lambda: faker.user_name()[:ArtistConsts.USERNAME_MAX_LENGTH])
    description = factory.LazyFunction(lambda: faker.text(max_nb_chars=ArtistConsts.DESCRIPTION_MAX_LENGTH))
    avatar = factory.django.ImageField(
        filename="test_image.jpg", width=200, height=200, color="blue", format="JPEG",
    )



class ArtistSongFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArtistSong
        django_get_or_create = ("artist", "song")

    artist = factory.SubFactory(ArtistFactory)
    song = factory.SubFactory(SongFactory)


class FavouriteArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavouriteArtist

    user = factory.SubFactory(UserFactory)
    artist = factory.SubFactory(ArtistFactory)
