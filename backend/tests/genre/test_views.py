from rest_framework import status

from django.urls import reverse

from .factories.model import GenreFactory
from ..base import (
    AuthenticatedAPITestCase,
    AnonymousAPITestCase,
)


class GenreListDetailViewSetAuthenticatedTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.genre = GenreFactory()
        cls.list_url = reverse("genre-list")
        cls.detail_url = reverse("genre-detail", kwargs={"pk": cls.genre.pk})

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_detail_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GenreListDetailViewSetAnonymousTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = GenreFactory()
        cls.list_url = reverse("genre-list")
        cls.detail_url = reverse("genre-detail", kwargs={"pk": cls.genre.pk})

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_detail_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GenreListsViewSetAnonymousUserTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = GenreFactory()
        cls.genre_artists_url = reverse("genre-lists-artists", kwargs={"pk": cls.genre.pk})
        cls.nonexistent_genre_artists_url = reverse("genre-lists-artists", kwargs={"pk": 999_999})
        cls.genre_albums_url = reverse("genre-lists-albums", kwargs={"pk": cls.genre.pk})
        cls.nonexistent_genre_albums_url = reverse("genre-lists-albums", kwargs={"pk": 999_999})

    def test_returns_200_for_genre_artists_list(self):
        response = self.client.get(self.genre_artists_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_genre_artists_list_for_nonexistent_genre(self):
        response = self.client.get(self.nonexistent_genre_artists_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_200_for_genre_albums_list(self):
        response = self.client.get(self.genre_albums_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_genre_albums_list_for_nonexistent_genre(self):
        response = self.client.get(self.nonexistent_genre_albums_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GenreListsViewSetAuthenticatedUserTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.genre = GenreFactory()
        cls.genre_artists_url = reverse("genre-lists-artists", kwargs={"pk": cls.genre.pk})
        cls.nonexistent_genre_artists_url = reverse("genre-lists-artists", kwargs={"pk": 999_999})
        cls.genre_albums_url = reverse("genre-lists-albums", kwargs={"pk": cls.genre.pk})
        cls.nonexistent_genre_albums_url = reverse("genre-lists-albums", kwargs={"pk": 999_999})

    def test_returns_200_for_genre_artists_list(self):
        response = self.client.get(self.genre_artists_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_genre_artists_list_for_nonexistent_genre(self):
        response = self.client.get(self.nonexistent_genre_artists_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_200_for_genre_albums_list(self):
        response = self.client.get(self.genre_albums_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_genre_albums_list_for_nonexistent_genre(self):
        response = self.client.get(self.nonexistent_genre_albums_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserGenreViewSetAuthenticatedUserTestCase(
    AuthenticatedAPITestCase
):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.genre = GenreFactory()
        cls.user_genre_url = reverse("user-genre-data", kwargs={"pk": cls.genre.pk})
        cls.user_nonexistent_genre_url = reverse("user-genre-data", kwargs={"pk": 999_999})

    def test_returns_200_for_existent_genre(self):
        response = self.client.get(self.user_genre_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_nonexistent_genre(self):
        response = self.client.get(self.user_nonexistent_genre_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserGenreViewSetAnonymousTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = GenreFactory()
        cls.user_genre_url = reverse("user-genre-data", kwargs={"pk": cls.genre.pk})

    def test_returns_404_for_existent_url(self):
        response = self.client.get(self.user_genre_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
