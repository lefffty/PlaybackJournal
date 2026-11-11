from django.urls import reverse
from rest_framework import status

from review.models import Review, ReviewComment

from tests.base import (
    AnonymousAPITestCase,
    AuthenticatedAPITestCase,
)
from tests.review.factories.model import ReviewFactory
from tests.users.factories.model import UserFactory
from tests.review.factories.form import ReviewDataFactory, ReviewCommentDataFactory
from tests.albums.factories.model import AlbumFactory


class ReviewModelViewSetAnonymousTest(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.album = AlbumFactory()
        cls.review = ReviewFactory(
            album=cls.album,
            author=cls.user,
        )
        cls.data = ReviewDataFactory(
            album=cls.album.pk,
        )
        cls.update_data = ReviewDataFactory(
            album=cls.album.pk
        )
        cls.create_url = reverse("review-list")
        cls.delete_url = reverse("review-detail", kwargs={"pk": cls.review.pk})
        cls.update_url = reverse("review-detail", kwargs={"pk": cls.review.pk})
        cls.retrieve_url = reverse("review-detail", kwargs={"pk": cls.review.pk})
        cls.retrieve_url_404 = reverse("review-comments", kwargs={"pk": 999_999})
        cls.retrieve_comments_url = reverse("review-comments", kwargs={"pk": cls.review.pk})

    def test_returns_200_for_retrieve_action_for_anonymous_user(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_401_for_create_action_for_anonymous_user(self):
        response = self.client.post(self.create_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_delete_action_for_anonymous_user(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_update_action_for_anonymous_user(self):
        response = self.client.put(self.update_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_200_for_retrieve_comments_action_for_anonymous_user(self):
        response = self.client.get(self.retrieve_comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_retrieve_comments_action_for_nonexistent_review_for_anonymous_user(self):
        response = self.client.get(self.retrieve_url_404)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReviewModelViewSetAuthenticatedTest(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.other_user = UserFactory()
        cls.album = AlbumFactory()
        cls.review = ReviewFactory(
            album=cls.album,
            author=cls.user,
        )
        cls.data = ReviewDataFactory(
            album=cls.album.pk,
        )
        cls.update_data = ReviewDataFactory(
            album=cls.album.pk
        )
        cls.create_url = reverse("review-list")
        cls.delete_url = reverse("review-detail", kwargs={"pk": cls.review.pk})
        cls.update_url = reverse("review-detail", kwargs={"pk": cls.review.pk})
        cls.retrieve_url = reverse("review-detail", kwargs={"pk": cls.review.pk})
        cls.retrieve_url_404 = reverse("review-comments", kwargs={"pk": 999_999})
        cls.retrieve_comments_url = reverse("review-comments", kwargs={"pk": cls.review.pk})

    def _check_reviews_count(self, expected_cnt: int):
        self.assertEqual(Review.objects.count(), expected_cnt)

    def test_returns_201_for_create_action_for_authenticated_user(self):
        response = self.client.post(self.create_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_reviews_count(2)

    def test_returns_204_for_delete_action_for_authorized_user(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._check_reviews_count(0)

    def test_returns_403_for_delete_action_for_unauthorized_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._check_reviews_count(1)

    def test_returns_200_for_retrieve_action_for_other_user(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_update_action_for_authorized_user(self):
        response = self.client.put(self.update_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._check_reviews_count(1)

    def test_returns_403_for_update_action_for_unauthorized_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(self.update_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_returns_200_for_retrieve_commments_action_for_authenticated_user(self):
        response = self.client.get(self.retrieve_comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_retrieve_comments_action_for_nonexistent_review_for_authenticated_user(self):
        response = self.client.get(self.retrieve_url_404)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReviewCommentViewSetAuthenticatedUserTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.review = ReviewFactory()
        cls.data = ReviewCommentDataFactory(
            author=cls.user.pk,
            review=cls.review.pk,
        )
        cls.create_url = reverse("review-comments-list")

    def _check_review_comments_count(self, review_id: int, expected_cnt: int):
        self.assertEqual(
            ReviewComment.objects.filter(review_id=review_id).count(),
            expected_cnt
        )

    def test_returns_201_for_create_comment_action(self):
        response = self.client.post(
            self.create_url, data=self.data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_review_comments_count(self.review.pk, 1)


class ReviewCommentViewSetAnonymousUserTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.review = ReviewFactory(
            author=cls.user
        )
        cls.data = ReviewCommentDataFactory(
            author=cls.user.pk,
            review=cls.review.pk,
        )
        cls.create_url = reverse("review-comments-list")

    def _check_review_comments_count(self, review_id: int, expected_cnt: int):
        self.assertEqual(
            ReviewComment.objects.filter(review_id=review_id).count(),
            expected_cnt
        )

    def test_returns_401_for_create_comment_action(self):
        response = self.client.post(self.create_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self._check_review_comments_count(self.review.pk, 0)
