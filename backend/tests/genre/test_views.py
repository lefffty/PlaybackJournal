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
