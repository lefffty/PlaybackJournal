from django.test import TestCase

from tests.playlist.factories.model import PlaylistFactory, RatedPlaylistFactory


class PlaylistModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.playlist = PlaylistFactory()
        cls.ratedplaylist1 = RatedPlaylistFactory(
            playlist=cls.playlist,
            rating=4,
        )
        cls.ratedplaylist2 = RatedPlaylistFactory(
            playlist=cls.playlist,
            rating=6,
        )

    def test_average_rating_property_returns_correct_data(self):
        actual = self.playlist.average_rating
        expected = 5
        self.assertEqual(actual, expected)

    def test_averate_rating_property_makes_only_one_query_to_database(self):
        with self.assertNumQueries(1):
            _ = self.playlist.average_rating
