from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SongsViewSet,
)

router = DefaultRouter()
router.register(
    r'songs',
    SongsViewSet,
    basename='songs',
)


urlpatterns = [
    path('', include(router.urls)),
]
