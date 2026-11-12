from rest_framework import status

from django.urls import reverse

from .factories.model import AlbumFactory
from .factories.form import AlbumCreateDataFactory
from ..genre.factories.model import GenreFactory
from ..artist.factories.model import ArtistFactory
from ..song.factories.form import SongCreateDataFactory
from ..base import (
    AuthenticatedAPITestCase,
    AnonymousAPITestCase,
)


class AlbumListDetailViewSetAnonymousUserTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.album = AlbumFactory()
        cls.data = AlbumCreateDataFactory()
        cls.list_url = reverse("albums-list")
        cls.detail_url = reverse("albums-detail", kwargs={"pk": cls.album.pk})
        cls.create_url = reverse("albums-list")
        cls.review_list_url = reverse("albums-reviews", kwargs={"pk": cls.album.pk})
        cls.statistics_url = reverse("albums-statistics", kwargs={"pk": cls.album.pk})

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_401_for_create_action(self):
        response = self.client.post(self.create_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_200_for_album_reviews(self):
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_album_statistics(self):
        response = self.client.get(self.statistics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AlbumListDetailViewSetAuthenticatedUserTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.song = SongCreateDataFactory()
        cls.genre = GenreFactory()
        cls.artist = ArtistFactory()
        cls.album = AlbumFactory()
        cls.list_url = reverse("albums-list")
        cls.detail_url = reverse("albums-detail", kwargs={"pk": cls.album.pk})
        cls.create_url = reverse("albums-list")
        cls.review_list_url = reverse("albums-reviews", kwargs={"pk": cls.album.pk})
        cls.statistics_url = reverse("albums-statistics", kwargs={"pk": cls.album.pk})
        cls.nonexistent_album_review_list_url = reverse("albums-reviews", kwargs={"pk": 999_999})
        cls.nonexistent_album_statistics_url = reverse("albums-statistics", kwargs={"pk": 999_999})

    def setUp(self):
        super().setUp()
        self.data = AlbumCreateDataFactory(
            songs=[song for song in [self.song]],
            genres=[{"id": genre.pk} for genre in [self.genre]],
            artists=[{"id": artist.pk} for artist in [self.artist]],
        )
        self.empty_song_data = AlbumCreateDataFactory(
            genres=[{"id": genre.pk} for genre in [self.genre]],
            artists=[{"id": artist.pk} for artist in [self.artist]],
        )
        self.empty_genres_data = AlbumCreateDataFactory(
            artists=[{"id": artist.pk} for artist in [self.artist]],
            songs=[song for song in [self.song]],
        )
        self.empty_artists_data = AlbumCreateDataFactory(
            songs=[song for song in [self.song]],
            genres=[{"id": genre.pk} for genre in [self.genre]],
        )

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_201_for_create_action(self):
        response = self.client.post(self.create_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_returns_400_for_create_action_if_songs_field_is_empty(self):
        response = self.client.post(self.create_url, data=self.empty_song_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_400_for_create_action_if_artists_is_empty(self):
        response = self.client.post(self.create_url, data=self.empty_artists_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_400_for_create_action_if_genres_is_empty(self):
        response = self.client.post(self.create_url, data=self.empty_genres_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_404_for_album_reviews_list_for_nonexistent_album(self):
        response = self.client.get(self.nonexistent_album_review_list_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_200_for_existent_album_reviews(self):
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_album_statistics_for_nonexistent_album(self):
        response = self.client.get(self.nonexistent_album_statistics_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_200_for_existent_album_statictics(self):
        response = self.client.get(self.statistics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
