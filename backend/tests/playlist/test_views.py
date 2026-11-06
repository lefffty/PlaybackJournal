from rest_framework import status

from django.urls import reverse
from django.db.models import Model

from playlist.models import (
    Playlist,
    RatedPlaylist,
    FavouritePlaylist,
)

from .factories.form import PlaylistCreateDataFactory, RatedPlaylistCreateDataFactory
from ..users.factories.model import UserFactory
from ..song.factories.model import SongFactory
from ..playlist.factories.model import PlaylistFactory
from ..base import (
    AuthenticatedAPITestCase,
    AnonymousAPITestCase
)


class PlaylistViewSetAuthenticatedTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user2 = UserFactory()
        cls.song = SongFactory()
        cls.playlist = PlaylistFactory(
            author=cls.user,
        )
        cls.data = PlaylistCreateDataFactory(
            songs=[{"id": song.id} for song in [cls.song]],
        )
        cls.update_data = PlaylistCreateDataFactory(
            songs=[{"id": song.id} for song in [cls.song]],
        )
        cls.list_url = reverse('playlist-list')
        cls.detail_url = reverse('playlist-detail', kwargs={"pk": cls.playlist.pk})
        cls.create_url = reverse('playlist-list')
        cls.update_url = reverse('playlist-detail', kwargs={"pk": cls.playlist.pk})

    def _check_playlist_count(self, expected):
        self.assertEqual(Playlist.objects.count(), expected)

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_201_for_create_action(self):
        response = self.client.post(self.create_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_playlist_count(2)

    def test_returns_200_for_update_action(self):
        response = self.client.patch(self.update_url, data=self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._check_playlist_count(1)

    def test_returns_403_for_update_action_if_current_user_is_not_author(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(self.update_url, data=self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._check_playlist_count(1)

    def test_returns_204_for_delete_action(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._check_playlist_count(0)

    def test_returns_403_for_delete_action_if_current_user_is_not_author(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._check_playlist_count(1)


class PlaylistViewSetAnonymousTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.song = SongFactory()
        cls.playlist = PlaylistFactory()
        cls.data = PlaylistCreateDataFactory(
            songs=[{"id": song.id} for song in [cls.song]],
        )
        cls.update_data = PlaylistCreateDataFactory(
            songs=[{"id": song.id} for song in [cls.song]],
        )
        cls.list_url = reverse('playlist-list')
        cls.detail_url = reverse('playlist-detail', kwargs={"pk": cls.playlist.pk})
        cls.create_url = reverse('playlist-list')
        cls.update_url = reverse('playlist-detail', kwargs={"pk": cls.playlist.pk})
        cls.delete_url = reverse('playlist-detail', kwargs={"pk": cls.playlist.pk})

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_401_for_create_action(self):
        response = self.client.post(self.create_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_update_action(self):
        response = self.client.put(self.update_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_delete_action(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PlaylistUserCreateViewSetAnonymousTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.playlist = PlaylistFactory()
        cls.data = RatedPlaylistCreateDataFactory()
        cls.rate_playlist_url = reverse('playlist-user-rated', kwargs={"pk": cls.playlist.pk})
        cls.favourite_playlist_url = reverse('playlist-user-favourite', kwargs={"pk": cls.playlist.pk})

    def test_returns_401_for_rate_playlist_endpoint(self):
        response = self.client.post(self.rate_playlist_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_favourite_playlist_endpoint(self):
        response = self.client.post(self.favourite_playlist_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PlaylistUserCreateViewSetAuthenticatedTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.playlist = PlaylistFactory()
        cls.data = RatedPlaylistCreateDataFactory()
        cls.invalid_data = RatedPlaylistCreateDataFactory(rating=-1)
        cls.update_data = RatedPlaylistCreateDataFactory()
        cls.rate_nonexistent_playlist_url = reverse('playlist-user-rated', kwargs={"pk": 100_000}),
        cls.favourite_nonexistent_playlist_url = reverse('playlist-user-favourite', kwargs={"pk": 100_000}),
        cls.rate_playlist_url = reverse('playlist-user-rated', kwargs={"pk": cls.playlist.pk})
        cls.favourite_playlist_url = reverse('playlist-user-favourite', kwargs={"pk": cls.playlist.pk})

    def _check_model_count(self, _Model: Model, expected_cnt: int):
        self.assertEqual(_Model.objects.count(), expected_cnt)

    def test_returns_201_for_rate_new_playlist_endpoint(self):
        response = self.client.post(self.rate_playlist_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_model_count(RatedPlaylist, 1)

    def test_returns_204_for_existing_playlist_endpoint(self):
        self.client.post(self.rate_playlist_url, data=self.data)
        self._check_model_count(RatedPlaylist, 1)
        response = self.client.post(self.rate_playlist_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._check_model_count(RatedPlaylist, 1)

    def test_returns_404_for_rate_playlist_endpoint_if_playlist_does_not_exist(self):
        response = self.client.post(self.rate_nonexistent_playlist_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_400_for_rate_playlist_endpoint_if_rating_data_is_empty(self):
        response = self.client.post(self.rate_playlist_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_400_for_rate_playlist_endpoint_if_rating_data_is_invalid(self):
        response = self.client.post(self.rate_playlist_url, data=self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_201_for_favourite_playlist_endpoint(self):
        response = self.client.post(self.favourite_playlist_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_model_count(FavouritePlaylist, 1)

    def test_returns_204_for_favourite_playlist_endpoint(self):
        self.client.post(self.favourite_playlist_url, data=self.data)
        self._check_model_count(FavouritePlaylist, 1)
        response = self.client.post(self.favourite_playlist_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._check_model_count(FavouritePlaylist, 0)

    def test_returns_404_for_favourite_playlist_endpoint_if_playlist_does_not_exist(self):
        response = self.client.post(self.favourite_nonexistent_playlist_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self._check_model_count(FavouritePlaylist, 0)
