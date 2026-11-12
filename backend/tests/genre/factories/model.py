import factory
from faker import Factory

from genre.models import Genre, FavouriteGenre
from genre.constants import GenreConsts
from tests.users.factories.model import UserFactory

faker = Factory.create()


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.LazyFunction(lambda: faker.word()[:GenreConsts.NAME_MAX_LENGTH])
    description = factory.LazyFunction(lambda: faker.text()[:GenreConsts.DESCRIPTION_MAX_LENGTH])


class FavouriteGenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavouriteGenre

    user = factory.SubFactory(UserFactory)
    genre = factory.SubFactory(GenreFactory)
