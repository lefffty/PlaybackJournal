from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (
    PlaylistSerializer,
    PlaylistCreateUpdateSerializer
)
from .permissions import OwnerOrReadOnly
from .models import Playlist


class PlaylistViewSet(
    viewsets.ModelViewSet
):
    queryset = Playlist.objects.all()
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'create'):
            return [IsAuthenticatedOrReadOnly()]
        return [OwnerOrReadOnly()]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PlaylistSerializer
        return PlaylistCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
