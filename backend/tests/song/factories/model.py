import factory
from datetime import datetime
from faker import Factory

from song.constants import SongConsts
from song.models import Song


faker = Factory.create()


class SongFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Song

    name = factory.LazyFunction(lambda: faker.name()[:SongConsts.NAME_MAX_LENGTH])
    duration = factory.LazyFunction(lambda: datetime.now().time().strftime("%H:%M:%S"))
