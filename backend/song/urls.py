from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SongsListRetrieveViewSet,
    UserSongPreferencesViewSet,
)

router = DefaultRouter()
router.register(
    r'songs',
    SongsListRetrieveViewSet,
    basename='songs',
)
router.register(
    r'songs',
    UserSongPreferencesViewSet,
    basename='song_user',
)


urlpatterns = [
    path('', include(router.urls)),
]
