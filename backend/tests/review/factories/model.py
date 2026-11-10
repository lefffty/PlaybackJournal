import factory
from faker import Factory

import django.utils.timezone as tz

from review.models import Review
from review.constants import ReviewConsts

from tests.albums.factories.model import AlbumFactory
from tests.users.factories.model import UserFactory

faker = Factory.create()


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    title = factory.LazyFunction(lambda: faker.name()[:ReviewConsts.TITLE_MAX_LENGTH])
    text = factory.LazyFunction(lambda: faker.text())
    type = "positive"
    author = factory.SubFactory(UserFactory)
    album = factory.SubFactory(AlbumFactory)
    created_at = factory.LazyFunction(tz.now)
    updated_at = factory.LazyFunction(tz.now)
