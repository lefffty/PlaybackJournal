from datetime import datetime

from django.test import TestCase

from tests.albums.factories.model import AlbumFactory, RatedAlbumFactory
from tests.review.factories.model import ReviewFactory
from tests.users.factories.model import UserFactory


class AlbumModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()
        cls.album = AlbumFactory()
        cls.ratedalbum1 = RatedAlbumFactory(
            user=cls.user1,
            album=cls.album,
            rating=4,
        )
        cls.ratedalbum2 = RatedAlbumFactory(
            user=cls.user2,
            album=cls.album,
            rating=6,
        )
        cls.review1 = ReviewFactory(
            author=cls.user1,
            album=cls.album,
            created_at=datetime(2024, 1, 1)
        )
        cls.review2 = ReviewFactory(
            author=cls.user2,
            album=cls.album,
            created_at=datetime(2024, 1, 3),
            type="negative",
        )
        cls.review2 = ReviewFactory(
            author=cls.user2,
            album=cls.album,
            created_at=datetime(2024, 1, 2),
            type="neutral",
        )

    def test_average_rating_returns_correct_value(self):
        actual = self.album.average_rating
        expected = 5
        self.assertEqual(actual, expected)

    def test_average_rating_does_only_one_query_to_database(self):
        with self.assertNumQueries(1):
            _ = self.album.average_rating

    def test_latest_reviews_property_returns_correct_data(self):
        actual_reviews = self.album.latest_reviews
        self.assertEqual(len(actual_reviews), 3)

    def test_latest_review_property_does_only_one_query_to_database(self):
        with self.assertNumQueries(1):
            _ = list(self.album.latest_reviews)

    def test_latest_reviews_has_sorting_by_created_at(self):
        qs = self.album.latest_reviews
        self.assertTrue(qs.query.order_by)
        self.assertEqual(qs.query.order_by, ('-created_at',))

    def test_reviews_statistics_property_returns_correct_data(self):
        actual = self.album.reviews_statistics
        expected = {
            "positive": 1,
            "neutral": 1,
            "negative": 1,
            "total": 3,
        }
        self.assertEqual(actual, expected)

    def test_reviews_statistics_property_does_only_one_query_to_database(self):
        with self.assertNumQueries(1):
            _ = list(self.album.reviews_statistics)
