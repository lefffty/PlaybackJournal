from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from tests.users.factories.model import UserFactory

User = get_user_model()


class AuthenticatedAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def setUp(self):
        self.client.force_authenticate(user=self.user)


class AnonymousAPITestCase(APITestCase):
    def setUp(self):
        self.client.force_authenticate(user=None)
