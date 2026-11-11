from django.urls import reverse
from django.db.models import Model
from rest_framework import status

from review.models import Review, ReviewComment, ReviewUserVote, CommentUserVote

from tests.base import (
    AnonymousAPITestCase,
    AuthenticatedAPITestCase,
)
from tests.review.factories.model import (
    ReviewFactory,
    ReviewCommentFactory,
    ReviewUserVoteFactory,
    CommentUserVoteFactory,
)
from tests.users.factories.model import UserFactory
from tests.review.factories.form import (
    ReviewDataFactory,
    ReviewCommentDataFactory,
    ReviewUserVoteDataFactory,
    CommentUserVoteDataFactory,
)
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


class ReactionViewSetAuthenticatedUserTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.other_user = UserFactory()
        cls.review = ReviewFactory(
            author=cls.user
        )
        cls.review_comment = ReviewCommentFactory(
            author=cls.user,
            review=cls.review,
        )
        cls.review_vote = ReviewUserVoteFactory(
            review=cls.review,
            user=cls.other_user,
        )
        cls.comment_vote = CommentUserVoteFactory(
            comment=cls.review_comment,
            user=cls.other_user,
        )
        cls.r_data = ReviewUserVoteDataFactory()
        cls.empty_r_data = ReviewUserVoteDataFactory(reaction='')
        cls.same_r_data = ReviewUserVoteDataFactory(reaction='not useful')
        cls.c_data = CommentUserVoteDataFactory()
        cls.empty_c_data = CommentUserVoteDataFactory(reaction='')
        cls.same_c_data = CommentUserVoteDataFactory(reaction='minus')
        cls.review_url = reverse("reactions-review", kwargs={"pk": cls.review.pk})
        cls.nonexistent_review_url = reverse("reactions-review", kwargs={"pk": 999_999})
        cls.comment_url = reverse("reactions-comment", kwargs={"pk": cls.review_comment.pk})
        cls.nonexistent_comment_url = reverse("reactions-comment", kwargs={"pk": 999_999})

    def _check_objects_count(self, _Model: Model, expected_cnt: int, **kwargs):
        self.assertEqual(
            _Model.objects.filter(**kwargs).count(),
            expected_cnt
        )

    def test_returns_404_for_nonexistent_review(self):
        response = self.client.post(self.nonexistent_review_url, data=self.r_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_400_for_reaction_to_review_if_reaction_value_was_not_provided(self):
        response = self.client.post(self.review_url, data=self.empty_r_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_201_for_new_reaction_to_review(self):
        response = self.client.post(self.review_url, data=self.r_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_objects_count(ReviewUserVote, 1, user=self.user, review=self.review)

    def test_returns_200_for_reaction_to_review_if_reaction_was_updated(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self.review_url, data=self.r_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._check_objects_count(ReviewUserVote, 0, user=self.user, review=self.review)

    def test_returns_204_for_reaction_to_review_if_reaction_is_same(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self.review_url, data=self.same_r_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._check_objects_count(ReviewUserVote, 0, user=self.other_user, review=self.review)

    def test_returns_404_for_nonexistent_comment(self):
        response = self.client.post(self.nonexistent_comment_url, data=self.c_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_400_for_reaction_to_comment_if_reaction_value_was_not_provided(self):
        response = self.client.post(self.comment_url, data=self.empty_c_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_201_for_new_reaction_to_comment(self):
        response = self.client.post(self.comment_url, data=self.c_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_objects_count(CommentUserVote, 1, user=self.user, comment=self.review_comment)

    def test_returns_200_for_reaction_to_comment_if_reaction_was_updated(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self.comment_url, data=self.c_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._check_objects_count(CommentUserVote, 0, user=self.user, comment=self.review_comment)

    def test_returns_204_for_reaction_to_comment_if_reaction_is_same(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self.comment_url, data=self.same_c_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._check_objects_count(CommentUserVote, 0, user=self.other_user, comment=self.review_comment)


class ReactionViewSetAnonymousUserTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.review = ReviewFactory(
            author=cls.user
        )
        cls.review_comment = ReviewCommentFactory(
            author=cls.user,
            review=cls.review,
        )
        cls.r_data = ReviewUserVoteDataFactory()
        cls.c_data = CommentUserVoteDataFactory()
        cls.review_url = reverse("reactions-review", kwargs={"pk": cls.review.pk})
        cls.comment_url = reverse("reactions-comment", kwargs={"pk": cls.review_comment.pk})

    def test_returns_401_for_review_reaction(self):
        response = self.client.post(self.review_url, self.r_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_comment_reaction(self):
        response = self.client.post(self.comment_url, self.c_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
