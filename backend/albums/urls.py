from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import AlbumViewSet


router = DefaultRouter()
router.register(
    r'albums',
    AlbumViewSet,
    basename='albums',
)

urlpatterns = [
    path('', include(router.urls)),
]
