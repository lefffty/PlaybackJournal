from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

import base64

from .factories.form import (
    NewPasswordDataFactory,
    UserCreateDataFactory,
    AvatarDataFactory,
)
from ..base import (
    AuthenticatedAPITestCase,
    AnonymousAPITestCase,
)

User = get_user_model()


class UserCreateViewSetTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("user-create-list")
        cls.create_data = UserCreateDataFactory()

    def _check_users_count(self, expected_cnt: int):
        self.assertEqual(User.objects.count(), expected_cnt)

    def test_returns_201(self):
        response = self.client.post(self.url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_users_count(1)


class UserProfileViewSetTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("user-profile-profile")

    def test_returns_401_for_not_authenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_returns_200_for_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AvatarViewSetTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("user-avatar-avatar")
        cls.data = AvatarDataFactory()

    def setUp(self):
        super().setUp()
        self._convert_avatar_to_base64()

    def _convert_avatar_to_base64(self):
        avatar = self.data["avatar"]
        avatar.seek(0)
        self.data["avatar"] = base64.b64encode(avatar.read()).decode("ascii")

    def _check_avatar_field_is_empty(self):
        self.user.refresh_from_db()
        self.assertFalse(self.user.avatar)

    def test_returns_401_for_not_authenticated_user(self):
        self.client.logout()
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_method_returns_200_for_authenticated_user(self):
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_method_returns_401_for_not_authenticated_user(self):
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_method_returns_204_for_authenticated_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_method_successfully_deletes_user_avatar(self):
        self.client.delete(self.url)
        self._check_avatar_field_is_empty()


class NewPasswordViewSetTestCase(AuthenticatedAPITestCase):
    plain_password = "testpass_1234"    

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("user-set-password")

    def setUp(self):
        super().setUp()
        self.data = NewPasswordDataFactory(current_password=self.plain_password)
        self.new = self.data["new_password"]

    def _check_password_was_changed(self, old_plain, new_plain):
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(old_plain))
        self.assertTrue(self.user.check_password(new_plain))

    def test_returns_401_for_not_authenticated_user(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_400_for_weak_password(self):
        new_weak_password = "1234"
        self.data["new_password"] = new_weak_password
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.plain_password))
        self.assertFalse(self.user.check_password(new_weak_password))

    def test_returns_204_for_correct_request(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_successfully_changes_password(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._check_password_was_changed(self.plain_password, self.new)


class UserListsViewSetAuthenticatedUserTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.reviews_list_url = reverse("user-list-reviews")
        cls.favourite_albums_list_url = reverse("user-list-favourite-albums")
        cls.wishlist_albums_list_url = reverse("user-list-wishlist-albums")
        cls.listened_albums_list_url = reverse("user-list-listened-albums")
        cls.rated_albums_list_url = reverse("user-list-rated-albums")
        cls.favourite_playlists_list_url = reverse("user-list-favourite-playlists")
        cls.rated_playlists_list_url = reverse("user-list-rated-playlists")
        cls.favourite_artists_list_url = reverse("user-list-favourite-artists")

    def test_returns_200_for_user_reviews_list(self):
        response = self.client.get(self.reviews_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_user_favourite_albums_list(self):
        response = self.client.get(self.favourite_albums_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_user_wishlist_albums_list(self):
        response = self.client.get(self.wishlist_albums_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_user_listened_albums_list(self):
        response = self.client.get(self.listened_albums_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_user_rated_albums_list(self):
        response = self.client.get(self.rated_albums_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_user_favourite_playlists_list(self):
        response = self.client.get(self.favourite_playlists_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_user_rated_playlists_list(self):
        response = self.client.get(self.rated_playlists_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_user_favourite_artists_list(self):
        response = self.client.get(self.favourite_artists_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserListsViewSetAnonymousUserTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reviews_list_url = reverse("user-list-reviews")
        cls.favourite_albums_list_url = reverse("user-list-favourite-albums")
        cls.wishlist_albums_list_url = reverse("user-list-wishlist-albums")
        cls.listened_albums_list_url = reverse("user-list-listened-albums")
        cls.rated_albums_list_url = reverse("user-list-rated-albums")
        cls.favourite_playlists_list_url = reverse("user-list-favourite-playlists")
        cls.rated_playlists_list_url = reverse("user-list-rated-playlists")
        cls.favourite_artists_list_url = reverse("user-list-favourite-artists")

    def test_returns_401_for_user_reviews_list(self):
        response = self.client.get(self.reviews_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_user_favourite_albums_list(self):
        response = self.client.get(self.favourite_albums_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_user_wishlist_albums_list(self):
        response = self.client.get(self.wishlist_albums_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_user_listened_albums_list(self):
        response = self.client.get(self.listened_albums_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_user_rated_albums_list(self):
        response = self.client.get(self.rated_albums_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_user_favourite_playlists_list(self):
        response = self.client.get(self.favourite_playlists_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_user_rated_playlists_list(self):
        response = self.client.get(self.rated_playlists_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_user_favourite_artists_list(self):
        response = self.client.get(self.favourite_artists_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
