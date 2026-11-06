import factory
from datetime import datetime
from faker import Factory

from song.constants import SongConsts


faker = Factory.create()


class SongCreateDataFactory(factory.DictFactory):
    name = factory.LazyFunction(lambda: faker.name()[:SongConsts.NAME_MAX_LENGTH])
    duration = factory.LazyFunction(lambda: datetime.now().time().strftime("%H:%M:%S"))
