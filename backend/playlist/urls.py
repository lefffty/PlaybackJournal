from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PlaylistViewSet,
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

urlpatterns = [
    path('', include(router.urls)),
]
