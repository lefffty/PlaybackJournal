from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import GenreListDetailViewSet


router = DefaultRouter()
router.register(
    r'genres',
    GenreListDetailViewSet,
    basename='genre_list_detail',
)

urlpatterns = [
    path('', include(router.urls)),
]
