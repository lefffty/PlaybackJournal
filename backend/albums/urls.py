from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    AlbumListDetailViewSet,
    AlbumUserViewSet,
)


router = DefaultRouter()
router.register(
    r'albums',
    AlbumListDetailViewSet,
    basename='albums_list',
)
router.register(
    r'albums',
    AlbumUserViewSet,
    basename='album_user',
)

urlpatterns = [
    path('', include(router.urls)),
]
