from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SongsListViewSet
)


urlpatterns = [
    path('songs/', SongsListViewSet.as_view({
        'get': 'list'
    }), name='songs-list'),
]
