from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ArtistViewSet,
    ArtistDiscographyViewSet,
    UserArtistsPreferencesViewSet,
)


router = DefaultRouter()
router.register(
    r'artists',
    ArtistViewSet,
    basename='artists_detail',
)
router.register(
    r'artists',
    ArtistDiscographyViewSet,
    basename='artists_discography',
)
router.register(
    r'artists',
    UserArtistsPreferencesViewSet,
    basename='user_artists_preferences',
)

urlpatterns = [
    path('', include(router.urls)),
]
