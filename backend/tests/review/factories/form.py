import factory
import django.utils.timezone as tz
from faker import Factory

from review.constants import ReviewConsts

faker = Factory.create()


class ReviewDataFactory(factory.DictFactory):
    title = factory.LazyFunction(lambda: faker.name()[:ReviewConsts.TITLE_MAX_LENGTH])
    text = factory.LazyFunction(lambda: faker.text())
    type = "positive"
    album = None


class ReviewCommentDataFactory(factory.DictFactory):
    text = factory.LazyFunction(lambda: faker.text())
    author = None
    review = None
    created_at = factory.LazyFunction(tz.now)
