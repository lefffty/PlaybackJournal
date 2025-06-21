from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from .serializers import PlaylistSerializer
from .models import Playlist


class PlaylistViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
