from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views


router = DefaultRouter()
router.register(
    r'genres',
    views.GenreListDetailViewSet,
    basename='genre_list_detail',
)
router.register(
    r'genres',
    views.GenreListsViewSet,
    basename='genre_lists',
)
router.register(
    r'genres',
    views.UserGenrePreferencesViewSet,
    basename='user_genre_preferences',
)
router.register(
    r'genres',
    views.UserGenreViewSet,
    basename='user_genre',
)

urlpatterns = [
    path('', include(router.urls)),
]
