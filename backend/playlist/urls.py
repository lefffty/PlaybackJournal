from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PlaylistViewSet,
    UserPlaylistViewSet,
    PlaylistUserCreateViewSet,
)

router = DefaultRouter()
router.register(
    r'playlists',
    PlaylistViewSet,
    basename='playlist',
)
router.register(
    r'playlists',
    PlaylistUserCreateViewSet,
    basename='playlist-user',
)
router.register(
    r'playlists',
    UserPlaylistViewSet,
    basename='user-playlist'
)

urlpatterns = [
    path('', include(router.urls)),
]
