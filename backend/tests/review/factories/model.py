import factory
from faker import Factory

import django.utils.timezone as tz

from review.models import Review, ReviewComment, ReviewUserVote, CommentUserVote
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


class ReviewCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReviewComment

    text = factory.LazyFunction(lambda: faker.text())
    author = factory.SubFactory(UserFactory)
    review = factory.SubFactory(ReviewFactory)
    created_at = factory.LazyFunction(tz.now)


class ReviewUserVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReviewUserVote

    review = factory.SubFactory(ReviewFactory)
    user = factory.SubFactory(UserFactory)
    reaction = 'not useful'


class CommentUserVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommentUserVote

    comment = factory.SubFactory(ReviewCommentFactory)
    user = factory.SubFactory(UserFactory)
    reaction = 'minus'
