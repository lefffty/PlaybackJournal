from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import GenreListDetailViewSet, GenreListsViewSet


router = DefaultRouter()
router.register(
    r'genres',
    GenreListDetailViewSet,
    basename='genre_list_detail',
)
router.register(
    r'genres',
    GenreListsViewSet,
    basename='genre_lists',
)

urlpatterns = [
    path('', include(router.urls)),
]
