from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

import base64

from .factories.form import (
    NewPasswordDataFactory,
    UserCreateDataFactory,
    AvatarDataFactory,
)
from .factories.model import UserFactory

User = get_user_model()


class UserCreateViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-create-list")
        cls.create_data = UserCreateDataFactory()
        cls.fields = (
            "first_name",
            "last_name",
            "username",
            "email",
        )

    def _check_users_count(self, expected_cnt: int):
        self.assertEqual(User.objects.count(), expected_cnt)

    def _check_response_data(self, response, expected):
        for field in self.fields:
            self.assertIn(field, response)
            self.assertEqual(response[field], expected[field], response)

    def test_returns_201(self):
        response = self.client.post(self.url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_response_data(response.data, self.create_data)
        self._check_users_count(1)


class UserProfileViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-profile-profile")
        cls.user = UserFactory()
        cls.fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'registration_date',
            'avatar',
        )

    def _check_response_data(self, response, expected):
        for field in self.fields:
            self.assertIn(field, response)
            if field not in ("registration_date", "avatar"):
                self.assertEqual(response[field], getattr(expected, field))

    def test_returns_401_for_not_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_returns_200_for_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_correct_user_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self._check_response_data(response.data, self.user)


class AvatarViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-avatar-avatar")
        cls.user = UserFactory()
        cls.fields = (
            "avatar",
        )
        cls.data = AvatarDataFactory()

    def _convert_avatar_to_base64(self):
        avatar = self.data["avatar"]
        avatar.seek(0)
        self.data["avatar"] = base64.b64encode(avatar.read()).decode("ascii")

    def _check_avatar_field_is_empty(self):
        self.user.refresh_from_db()
        self.assertFalse(self.user.avatar)

    def _check_response_data(self, response):
        for field in self.fields:
            self.assertIn(field, response)

    def test_returns_401_for_not_authenticated_user(self):
        self._convert_avatar_to_base64()
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_method_returns_200_for_authenticated_user(self):
        self._convert_avatar_to_base64()
        self.client.force_authenticate(user=self.user)  
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_method_returns_correct_response_data(self):
        self._convert_avatar_to_base64()
        self.client.force_authenticate(user=self.user)  
        response = self.client.put(self.url, data=self.data)
        self._check_response_data(response.data)

    def test_delete_method_returns_401_for_not_authenticated_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_method_returns_204_for_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_method_successfully_deletes_user_avatar(self):
        self.client.force_authenticate(user=self.user)
        self.client.delete(self.url)
        self._check_avatar_field_is_empty()


class NewPasswordViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.plain_password = "testpass_1234"
        cls.user = UserFactory()
        cls.url = reverse("user-set-password")
        cls.data = NewPasswordDataFactory(current_password=cls.plain_password)
        cls.new = cls.data["new_password"]

    def _check_password_was_changed(self, initial, new):
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.password, initial)
        self.assertTrue(self.user.check_password(new))

    def test_returns_401_for_not_authenticated_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_400_for_weak_password(self):
        self.data["new_password"] = "1234"
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_204_for_correct_request(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content.decode())

    def test_successfully_changes_password(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, data=self.data)
        self._check_password_was_changed(self.plain_password, self.new)
