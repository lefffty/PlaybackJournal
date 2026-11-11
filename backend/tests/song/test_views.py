from rest_framework import status

from django.urls import reverse

from song.models import RatedSong

from tests.song.factories.model import SongFactory, RatedSongFactory
from tests.base import AuthenticatedAPITestCase, AnonymousAPITestCase
from tests.song.factories.form import RatedSongDataFactory


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


class UserSongPreferencesViewSetAuthenticatedUserTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.song1 = SongFactory()
        cls.song2 = SongFactory()
        cls.rated_song = RatedSongFactory(
            user=cls.user,
            song=cls.song2,
            rating=5,
        )
        cls.empty_rating_data = RatedSongDataFactory(rating=None)
        cls.invalid_rating_data = RatedSongDataFactory(rating=-1)
        cls.new_rating_data = RatedSongDataFactory()
        cls.same_rating_data = RatedSongDataFactory(rating=5)
        cls.new_rated_song_url = reverse("song_user-rated", kwargs={"pk": cls.song1.pk})
        cls.existent_rated_song_url = reverse("song_user-rated", kwargs={"pk": cls.song2.pk})
        cls.nonexistent_rated_song_url = reverse("song_user-rated", kwargs={"pk": 999_999})

    def _check_objects_count(self, expected_cnt: int, **kwargs):
        self.assertEqual(
            RatedSong.objects.filter(**kwargs).count(),
            expected_cnt,
        )

    def test_returns_404_for_nonexistent_song(self):
        response = self.client.post(self.nonexistent_rated_song_url, data=self.new_rating_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_returns_400_for_empty_rating_data(self):
        response = self.client.post(self.new_rated_song_url, data=self.empty_rating_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_400_for_invalid_rating_data(self):
        response = self.client.post(self.new_rated_song_url, data=self.invalid_rating_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_201_for_new_rating_record(self):
        response = self.client.post(self.new_rated_song_url, data=self.new_rating_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._check_objects_count(1, user=self.user, song=self.song1)

    def test_returns_200_for_existing_rating_record_if_rating_is_not_same(self):
        response = self.client.post(self.existent_rated_song_url, data=self.new_rating_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._check_objects_count(1, user=self.user, song=self.song2)

    def test_returns_204_for_existing_rating_record_if_rating_is_same(self):
        response = self.client.post(self.existent_rated_song_url, data=self.same_rating_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._check_objects_count(0, user=self.user, song=self.song2)


class UserSongPreferencesViewSetAnonymousUserTestCase(AnonymousAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.song1 = SongFactory()
        cls.new_rating_data = RatedSongDataFactory()
        cls.new_rated_song_url = reverse("song_user-rated", kwargs={"pk": cls.song1.pk})

    def test_returns_401_for_rate_song_action(self):
        response = self.client.post(self.new_rated_song_url, data=self.new_rating_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
