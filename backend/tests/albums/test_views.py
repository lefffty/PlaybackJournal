from django.db.models.base import Model
from rest_framework import status

from django.urls import reverse

from .factories.model import AlbumFactory, FavouriteAlbumFactory, RatedAlbumFactory, ListenedAlbumFactory, \
    WishlistAlbumFactory
from .factories.form import AlbumCreateDataFactory, RatedAlbumDataFactory
from ..genre.factories.model import GenreFactory
from ..artist.factories.model import ArtistFactory
from ..song.factories.form import SongCreateDataFactory
from ..base import (
    AuthenticatedAPITestCase,
    AnonymousAPITestCase,
)


class AlbumListDetailViewSetAnonymousUserTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.album = AlbumFactory()
        cls.data = AlbumCreateDataFactory()
        cls.list_url = reverse("albums-list")
        cls.detail_url = reverse("albums-detail", kwargs={"pk": cls.album.pk})
        cls.create_url = reverse("albums-list")
        cls.review_list_url = reverse("albums-reviews", kwargs={"pk": cls.album.pk})
        cls.statistics_url = reverse("albums-statistics", kwargs={"pk": cls.album.pk})

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_401_for_create_action(self):
        response = self.client.post(self.create_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_200_for_album_reviews(self):
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_album_statistics(self):
        response = self.client.get(self.statistics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AlbumListDetailViewSetAuthenticatedUserTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.song = SongCreateDataFactory()
        cls.genre = GenreFactory()
        cls.artist = ArtistFactory()
        cls.album = AlbumFactory()
        cls.list_url = reverse("albums-list")
        cls.detail_url = reverse("albums-detail", kwargs={"pk": cls.album.pk})
        cls.create_url = reverse("albums-list")
        cls.review_list_url = reverse("albums-reviews", kwargs={"pk": cls.album.pk})
        cls.statistics_url = reverse("albums-statistics", kwargs={"pk": cls.album.pk})
        cls.nonexistent_album_review_list_url = reverse("albums-reviews", kwargs={"pk": 999_999})
        cls.nonexistent_album_statistics_url = reverse("albums-statistics", kwargs={"pk": 999_999})

    def setUp(self):
        super().setUp()
        self.data = AlbumCreateDataFactory(
            songs=[song for song in [self.song]],
            genres=[{"id": genre.pk} for genre in [self.genre]],
            artists=[{"id": artist.pk} for artist in [self.artist]],
        )
        self.empty_song_data = AlbumCreateDataFactory(
            genres=[{"id": genre.pk} for genre in [self.genre]],
            artists=[{"id": artist.pk} for artist in [self.artist]],
        )
        self.empty_genres_data = AlbumCreateDataFactory(
            artists=[{"id": artist.pk} for artist in [self.artist]],
            songs=[song for song in [self.song]],
        )
        self.empty_artists_data = AlbumCreateDataFactory(
            songs=[song for song in [self.song]],
            genres=[{"id": genre.pk} for genre in [self.genre]],
        )

    def test_returns_200_for_retrieve_action(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_200_for_list_action(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_201_for_create_action(self):
        response = self.client.post(self.create_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_returns_400_for_create_action_if_songs_field_is_empty(self):
        response = self.client.post(self.create_url, data=self.empty_song_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_400_for_create_action_if_artists_is_empty(self):
        response = self.client.post(self.create_url, data=self.empty_artists_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_400_for_create_action_if_genres_is_empty(self):
        response = self.client.post(self.create_url, data=self.empty_genres_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_404_for_album_reviews_list_for_nonexistent_album(self):
        response = self.client.get(self.nonexistent_album_review_list_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_200_for_existent_album_reviews(self):
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_404_for_album_statistics_for_nonexistent_album(self):
        response = self.client.get(self.nonexistent_album_statistics_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_200_for_existent_album_statictics(self):
        response = self.client.get(self.statistics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserAlbumViewSetAuthenticatedUserTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.album = AlbumFactory()
        cls.existent_user_album_data_url = reverse("albums-status", kwargs={"pk": cls.album.pk})
        cls.nonexistent_user_album_data_url = reverse("albums-status", kwargs={"pk": 999_999})

    def test_returns_404_for_nonexistent_album(self):
        response = self.client.get(self.nonexistent_user_album_data_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_200_for_existent_album(self):
        response = self.client.get(self.existent_user_album_data_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserAlbumViewSetAnonymousUserTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.album = AlbumFactory()
        cls.existent_user_album_data_url = reverse("albums-status", kwargs={"pk": cls.album.pk})

    def test_returns_401_for_anonymous_user(self):
        response = self.client.get(self.existent_user_album_data_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAlbumsPreferencesViewSetAuthenticatedUserTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.album1 = AlbumFactory()
        cls.album2 = AlbumFactory()
        cls.favourite_album = FavouriteAlbumFactory(
            album=cls.album2,
            user=cls.user,
        )
        cls.rated_album = RatedAlbumFactory(
            album=cls.album2,
            user=cls.user,
            rating=5,
        )
        cls.listened_album = ListenedAlbumFactory(
            album=cls.album2,
            user=cls.user,
        )
        cls.wishlist_album = WishlistAlbumFactory(
            album=cls.album2,
            user=cls.user,
        )
        cls.data = RatedAlbumDataFactory(rating=3)
        cls.empty_data = RatedAlbumDataFactory(rating=None)
        cls.invalid_data = RatedAlbumDataFactory(rating=-1)
        cls.same_data = RatedAlbumDataFactory()
        cls.new_favour_album_url = reverse("albums-favourite", kwargs={"pk": cls.album1.pk})
        cls.new_rate_album_url = reverse("albums-rated", kwargs={"pk": cls.album1.pk})
        cls.new_listened_album_url = reverse("albums-listened", kwargs={"pk": cls.album1.pk})
        cls.new_wishlist_album_url = reverse("albums-wishlist", kwargs={"pk": cls.album1.pk})
        cls.nonexistent_favour_album_url = reverse("albums-favourite", kwargs={"pk": 999_999})
        cls.nonexistent_rate_album_url = reverse("albums-rated", kwargs={"pk": 999_999})
        cls.nonexistent_listened_album_url = reverse("albums-listened", kwargs={"pk": 999_999})
        cls.nonexistent_wishlist_album_url = reverse("albums-wishlist", kwargs={"pk": 999_999})
        cls.existent_favour_album_url = reverse("albums-favourite", kwargs={"pk": cls.album2.pk})
        cls.existent_rate_album_url = reverse("albums-rated", kwargs={"pk": cls.album2.pk})
        cls.existent_listened_album_url = reverse("albums-listened", kwargs={"pk": cls.album2.pk})
        cls.existent_wishlist_album_url = reverse("albums-wishlist", kwargs={"pk": cls.album2.pk})

    def _check_model_count(self, _Model: Model, expected_cnt: int, **filter_kwargs):
        self.assertEqual(
            _Model.objects.filter(**filter_kwargs).count(),
            expected_cnt)

    def test_returns_404_for_favourite_nonexistent_album(self):
        response = self.client.post(self.nonexistent_favour_album_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_201_for_new_favourite_album_record(self):
        response = self.client.post(self.new_favour_album_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_returns_204_for_existing_favourite_album_record(self):
        response = self.client.post(self.existent_favour_album_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_returns_404_for_rated_nonexistent_album(self):
        response = self.client.post(self.nonexistent_rate_album_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_400_for_empty_rated_album_data(self):
        response = self.client.post(self.new_rate_album_url, data=self.empty_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_400_for_invalid_rated_album_data(self):
        response = self.client.post(self.new_rate_album_url, data=self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_201_for_new_rated_album_record(self):
        response = self.client.post(self.new_rate_album_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_returns_200_for_existing_rated_album_record_if_rating_is_not_same(self):
        response = self.client.post(self.existent_rate_album_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_204_for_existing_rated_album_record_if_rating_is_same(self):
        response = self.client.post(self.existent_rate_album_url, data=self.same_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_returns_404_for_listened_nonexistent_album(self):
        response = self.client.post(self.nonexistent_listened_album_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_201_for_new_listened_album_record(self):
        response = self.client.post(self.new_listened_album_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_returns_204_for_existing_listened_album_record(self):
        response = self.client.post(self.existent_listened_album_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_returns_404_for_wishlist_nonexistent_album(self):
        response = self.client.post(self.nonexistent_wishlist_album_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_201_for_new_wishlist_album_record(self):
        response = self.client.post(self.new_wishlist_album_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_returns_204_for_existing_wishlist_album_record(self):
        response = self.client.post(self.existent_wishlist_album_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserAlbumsPreferencesViewSetAnonymousUserTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.album = AlbumFactory()
        cls.data = RatedAlbumDataFactory()
        cls.favour_album_url = reverse("albums-favourite", kwargs={"pk": cls.album.pk})
        cls.rate_album_url = reverse("albums-rated", kwargs={"pk": cls.album.pk})
        cls.listened_album_url = reverse("albums-listened", kwargs={"pk": cls.album.pk})
        cls.wishlist_album_url = reverse("albums-wishlist", kwargs={"pk": cls.album.pk})

    def test_returns_401_for_rate_album_route(self):
        response = self.client.post(self.favour_album_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_listen_album_route(self):
        response = self.client.post(self.listened_album_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_wishlist_album_route(self):
        response = self.client.post(self.wishlist_album_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_401_for_favourite_album_route(self):
        response = self.client.post(self.favour_album_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
