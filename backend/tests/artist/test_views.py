from django.urls import reverse
from rest_framework import status

from .factories.model import ArtistFactory, FavouriteArtistFactory
from ..base import (
    AuthenticatedAPITestCase,
    AnonymousAPITestCase
)


class ArtistViewSetAuthenticatedTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.artist = ArtistFactory()
        cls.artist2 = ArtistFactory()
        cls.fav_artist = FavouriteArtistFactory(
            artist=cls.artist2,
            user=cls.user
        )
        cls.list_url = reverse("artist-list")
        cls.detail_url = reverse("artist-detail", kwargs={"pk": cls.artist.pk})
        cls.discography_url = reverse("artist-discography", kwargs={"pk": cls.artist.pk})
        cls.similar_url = reverse("artist-similar", kwargs={"pk": cls.artist.pk})
        cls.favourite_url = reverse("artist-favourite", kwargs={"pk": cls.artist.pk})
        cls.favourite_delete_url = reverse("artist-favourite", kwargs={"pk": cls.artist2.pk})

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_artist_discography_action(self):
        response = self.client.get(self.discography_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_artist_similar_action(self):
        response = self.client.get(self.similar_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_get_method_for_favourite_action(self):
        response = self.client.get(self.favourite_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_201_for_post_method_for_favourite_action(self):
        response = self.client.post(self.favourite_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_returns_204_for_delete_method_for_favourite_action(self):
        response = self.client.delete(self.favourite_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ArtistViewSetAnonymousTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.artist = ArtistFactory()
        cls.list_url = reverse("artist-list")
        cls.detail_url = reverse("artist-detail", kwargs={"pk": cls.artist.pk})
        cls.discography_url = reverse("artist-discography", kwargs={"pk": cls.artist.pk})
        cls.similar_url = reverse("artist-similar", kwargs={"pk": cls.artist.pk})
        cls.favourite_url = reverse("artist-favourite", kwargs={"pk": cls.artist.pk})

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_artist_discography_action(self):
        response = self.client.get(self.discography_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_artist_similar_action(self):
        response = self.client.get(self.similar_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_401_for_get_method_for_favourite_action(self):
        response = self.client.get(self.favourite_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_post_method_for_favourite_action(self):
        response = self.client.post(self.favourite_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_delete_method_for_favourite_action(self):
        response = self.client.delete(self.favourite_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
