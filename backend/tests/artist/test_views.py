from django.urls import reverse
from rest_framework import status

from .factories.model import ArtistFactory
from ..base import (
    AuthenticatedAPITestCase,
    AnonymousAPITestCase
)


class ArtistViewSetAuthenticatedTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.artist = ArtistFactory()
        cls.list_url = reverse("artists-list")
        cls.detail_url = reverse("artists-detail", kwargs={"pk": cls.artist.pk})

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ArtistViewSetAnonymousTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.artist = ArtistFactory()
        cls.list_url = reverse("artists-list")
        cls.detail_url = reverse("artists-detail", kwargs={"pk": cls.artist.pk})

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
