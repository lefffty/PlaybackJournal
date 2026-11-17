from django.test import TestCase

from genre.constants import GenreConsts

from tests.genre.factories.model import GenreFactory
from tests.artist.factories.model import ArtistGenreFactory
from tests.albums.factories.model import AlbumGenreFactory


class GenreModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = GenreFactory()
        cls.genre_albums = AlbumGenreFactory.create_batch(
            GenreConsts.ALBUMS_LIMIT + 1,
            genre=cls.genre,
        )
        cls.genre_artists = ArtistGenreFactory.create_batch(
            GenreConsts.ARTISTS_LIMIT + 1,
            genre=cls.genre,
        )

    def test_limited_albums_property_returns_correct_data(self):
        limited_albums = self.genre.limited_albums
        self.assertEqual(len(limited_albums), GenreConsts.ALBUMS_LIMIT)

    def test_limited_albums_property_sorting(self):
        qs = self.genre.limited_albums
        self.assertFalse(qs.query.order_by)

    def test_limited_artists_property_does_only_one_query_to_database(self):
        with self.assertNumQueries(2):
            _ = list(self.genre.limited_albums)

    def test_limited_artists_property_returns_correct_data(self):
        limited_artists = self.genre.limited_artists
        self.assertEqual(len(limited_artists), GenreConsts.ARTISTS_LIMIT)

    def test_limited_artists_property_sorting(self):
        qs = self.genre.limited_artists
        self.assertFalse(qs.query.order_by)

    def test_limited_albums_property_does_only_one_query_to_database(self):
        with self.assertNumQueries(1):
            _ = list(self.genre.limited_artists)
