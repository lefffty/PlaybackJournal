import factory
from datetime import datetime
from faker import Factory

from song.constants import SongConsts, RatedSongConsts
from song.models import Song, RatedSong

from tests.users.factories.model import UserFactory

faker = Factory.create()


class SongFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Song

    name = factory.LazyFunction(lambda: faker.name()[:SongConsts.NAME_MAX_LENGTH])
    duration = factory.LazyFunction(lambda: datetime.now().time().strftime("%H:%M:%S"))


class RatedSongFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RatedSong

    user = factory.SubFactory(UserFactory)
    song = factory.SubFactory(SongFactory)
    rating = factory.LazyFunction(
        lambda: faker.pyint(
            min_value=RatedSongConsts.MIN_RATING,
            max_value=RatedSongConsts.MAX_RATING
        )
    )
