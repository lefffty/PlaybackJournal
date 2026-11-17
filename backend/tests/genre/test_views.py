from rest_framework import status

from django.urls import reverse

from genre.models import FavouriteGenre

from tests.genre.factories.model import GenreFactory, FavouriteGenreFactory
from tests.base import AuthenticatedAPITestCase, AnonymousAPITestCase


class GenreViewSetAuthenticatedTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.genre = GenreFactory()
        cls.genre2 = GenreFactory()
        cls.favourite_genre = FavouriteGenreFactory(
            user=cls.user,
            genre=cls.genre2,
        )
        cls.list_url = reverse("genre-list")
        cls.detail_url = reverse("genre-detail", kwargs={"pk": cls.genre.pk})
        cls.genre_artists_url = reverse("genre-artists", kwargs={"pk": cls.genre.pk})
        cls.nonexistent_genre_artists_url = reverse("genre-artists", kwargs={"pk": 999_999})
        cls.genre_albums_url = reverse("genre-albums", kwargs={"pk": cls.genre.pk})
        cls.nonexistent_genre_albums_url = reverse("genre-albums", kwargs={"pk": 999_999})
        cls.favourite_genre_url = reverse("genre-favourite", kwargs={"pk": cls.genre.pk})
        cls.nonexistent_genre_url = reverse("genre-favourite", kwargs={"pk": 999_999})
        cls.existent_genre_url = reverse("genre-favourite", kwargs={"pk": cls.genre2.pk})

    def _check_model_count(self, expected_cnt: int, **filter_kwargs):
        self.assertEqual(
            FavouriteGenre.objects.filter(**filter_kwargs).count(),
            expected_cnt
        )

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_detail_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_returns_200_for_existent_genre(self):
        response = self.client.get(self.favourite_genre_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_nonexistent_genre(self):
        response = self.client.get(self.nonexistent_genre_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_201_for_new_favourite_genre_record(self):
        response = self.client.post(self.favourite_genre_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_model_count(2, user=self.user)

    def test_returns_204_for_existent_favourite_genre_record(self):
        response = self.client.delete(self.existent_genre_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._check_model_count(0, user=self.user)


class GenreViewSetAnonymousTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = GenreFactory()
        cls.list_url = reverse("genre-list")
        cls.detail_url = reverse("genre-detail", kwargs={"pk": cls.genre.pk})
        cls.genre_artists_url = reverse("genre-artists", kwargs={"pk": cls.genre.pk})
        cls.nonexistent_genre_artists_url = reverse("genre-artists", kwargs={"pk": 999_999})
        cls.genre_albums_url = reverse("genre-albums", kwargs={"pk": cls.genre.pk})
        cls.nonexistent_genre_albums_url = reverse("genre-albums", kwargs={"pk": 999_999})
        cls.new_favour_genre_url = reverse("genre-favourite", kwargs={"pk": cls.genre.pk})

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_detail_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_returns_401(self):
        response = self.client.post(self.new_favour_genre_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GenreViewSetPerformanceTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.genre = GenreFactory()
        cls.genre2 = GenreFactory()
        cls.genre3 = GenreFactory()
        cls.genre4 = GenreFactory()
        cls.favour_genre = FavouriteGenreFactory(user=cls.user, genre=cls.genre)
        cls.list_url = reverse("genre-list")
        cls.detail_url = reverse("genre-detail", kwargs={"pk": cls.genre.pk})
        cls.genre_artists_url = reverse("genre-artists", kwargs={"pk": cls.genre.pk})
        cls.genre_albums_url = reverse("genre-albums", kwargs={"pk": cls.genre.pk})
        cls.genre_favour_url = reverse("genre-favourite", kwargs={"pk": cls.genre.pk})
        cls.genre_favour_delete_url = reverse("genre-favourite", kwargs={"pk": cls.genre2.pk})

    def test_genre_list_number_of_made_queries(self):
        with self.assertNumQueries(2):
            _ = self.client.get(self.list_url)

    def test_genre_detail_number_of_made_queries(self):
        with self.assertNumQueries(4):
            _ = self.client.get(self.detail_url)

    def test_genre_artists_list_number_of_made_queries(self):
        with self.assertNumQueries(2):
            _ = self.client.get(self.genre_artists_url)

    def test_genre_albums_list_number_of_made_queries(self):
        with self.assertNumQueries(2):
            _ = self.client.get(self.genre_albums_url)

    def test_favour_genre_GET_method_number_of_made_queries(self):
        with self.assertNumQueries(2):
            _ = self.client.get(self.genre_favour_url)

    def test_favour_genre_POST_method_number_of_made_queries(self):
        with self.assertNumQueries(2):
            _ = self.client.post(self.genre_favour_url)

    def test_favour_genre_DELETE_method_number_of_made_queries(self):
        with self.assertNumQueries(2):
            _ = self.client.delete(self.genre_favour_delete_url)
