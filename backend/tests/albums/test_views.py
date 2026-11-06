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


class AlbumListDetailViewSetAnonymousTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.album = AlbumFactory()
        cls.data = AlbumCreateDataFactory()
        cls.list_url = reverse("albums-list")
        cls.detail_url = reverse("albums-detail", kwargs={"pk": cls.album.pk})
        cls.create_url = reverse("albums-list")

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_401_for_create_action(self):
        response = self.client.post(self.create_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AlbumListDetailViewSetAuthenticatedTestCase(AuthenticatedAPITestCase):
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content.decode())

    def test_returns_400_for_create_action_if_songs_field_is_empty(self):
        response = self.client.post(self.create_url, data=self.empty_song_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content.decode())

    def test_returns_400_for_create_action_if_artists_is_empty(self):
        response = self.client.post(self.create_url, data=self.empty_artists_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content.decode())

    def test_returns_400_for_create_action_if_genres_is_empty(self):
        response = self.client.post(self.create_url, data=self.empty_genres_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content.decode())
