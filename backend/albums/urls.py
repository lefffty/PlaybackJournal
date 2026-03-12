from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    AlbumListDetailViewSet,
    UserAlbumsPreferencesViewSet,
    UserAlbumViewSet
)


router = DefaultRouter()
router.register(
    r'albums',
    AlbumListDetailViewSet,
    basename='albums_list',
)
router.register(
    r'albums',
    UserAlbumsPreferencesViewSet,
    basename='album_user',
)
router.register(
    r'albums',
    UserAlbumViewSet,
    basename='user_album',
)

urlpatterns = [
    path('', include(router.urls)),
]
