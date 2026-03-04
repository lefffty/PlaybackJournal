from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SongsListRetrieveViewSet
)

router = DefaultRouter()
router.register(
    r'songs',
    SongsListRetrieveViewSet,
    basename='songs',
)


urlpatterns = [
    path('', include(router.urls)),
]
