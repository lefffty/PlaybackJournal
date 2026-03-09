from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PlaylistViewSet,
    UserPlaylistViewSet,
    PlaylistCreateUserViewSet,
)

router = DefaultRouter()
router.register(
    r'playlists',
    PlaylistViewSet,
    basename='playlist',
)
router.register(
    r'playlists',
    PlaylistCreateUserViewSet,
    basename='playlist_user',
)
router.register(
    r'playlists',
    UserPlaylistViewSet,
    basename='user_playlist'
)

urlpatterns = [
    path('', include(router.urls)),
]
