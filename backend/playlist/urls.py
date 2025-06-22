from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PlaylistListDetailViewSet,
    PlaylistCreateUpdateViewSet
)

router = DefaultRouter()
router.register(
    r'playlists',
    PlaylistCreateUpdateViewSet,
    basename='playlist_create_update',
)
router.register(
    r'playlists',
    PlaylistListDetailViewSet,
    basename='playlist_list_detail',
)


urlpatterns = [
    path('', include(router.urls)),
]
