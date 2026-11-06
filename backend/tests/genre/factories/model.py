import factory
from faker import Factory

from genre.models import Genre
from genre.constants import GenreConsts

faker = Factory.create()


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.LazyFunction(lambda: faker.word()[:GenreConsts.NAME_MAX_LENGTH])
    description = factory.LazyFunction(lambda: faker.text()[:GenreConsts.DESCRIPTION_MAX_LENGTH])
