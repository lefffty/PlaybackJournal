from django.test import TestCase

from artist.constants import ArtistConsts

from tests.artist.factories.model import ArtistFactory, RelatedArtistsFactory
from tests.albums.factories.model import AlbumArtistFactory


class ArtistModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.artist = ArtistFactory()
        cls.artist_album = AlbumArtistFactory.create_batch(ArtistConsts.ALBUMS_LIMIT + 1, artist=cls.artist)
        cls.similar_artists = RelatedArtistsFactory.create_batch(ArtistConsts.ARTISTS_LIMIT + 1, artist=cls.artist)

    def test_earliest_albums_propert_returns_correct_data(self):
        albums = self.artist.earliest_albums
        self.assertEqual(len(albums), ArtistConsts.ALBUMS_LIMIT)

    def test_earliest_albums_property_does_only_one_query_to_database(self):
        with self.assertNumQueries(1):
            _ = list(self.artist.earliest_albums)

    def test_earliest_albums_property_ordering(self):
        qs = self.artist.earliest_albums
        self.assertTrue(qs.query.order_by)
        self.assertEqual(qs.query.order_by, ("publication_date",))

    def test_similar_property_returns_correct_data(self):
        artists = self.artist.similar
        self.assertEqual(len(artists), ArtistConsts.ARTISTS_LIMIT)

    def test_similar_property_does_only_one_query_to_database(self):
        with self.assertNumQueries(1):
            _ = list(self.artist.similar)

    def test_similar_property_ordering(self):
        qs = self.artist.similar
        self.assertTrue(qs.query.order_by)
        self.assertEqual(qs.query.order_by, ("id",))
