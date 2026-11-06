from rest_framework import status

from django.urls import reverse

from .factories.model import SongFactory
from ..base import AuthenticatedAPITestCase, AnonymousAPITestCase


class SongsListRetrieveViewSetAuthenticatedTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.song = SongFactory()
        cls.list_url = reverse("songs-list")
        cls.detail_url = reverse("songs-detail", kwargs={"pk": cls.song.pk})

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_status_code_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SongsListRetrieveViewSetAnonymousTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.song = SongFactory()
        cls.list_url = reverse("songs-list")
        cls.detail_url = reverse("songs-detail", kwargs={"pk": cls.song.pk})

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_status_code_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
