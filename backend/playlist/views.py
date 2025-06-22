from rest_framework import viewsets, mixins
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    PlaylistSerializer,
    PlaylistCreateUpdateSerializer
)
from .models import Playlist


class PlaylistListDetailViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class PlaylistCreateUpdateViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = PlaylistCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Playlist.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
