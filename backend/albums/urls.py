from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import AlbumListDetailViewSet


router = DefaultRouter()
router.register(
    r'albums',
    AlbumListDetailViewSet,
    basename='albums',
)

urlpatterns = [
    path('', include(router.urls)),
]
