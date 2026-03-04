from rest_framework import viewsets, mixins

from .models import Song
from .serializers import (
    SongListSerializer,
    SongSerializer
)


class SongsListRetrieveViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = Song.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ('list'):
            return SongListSerializer
        return SongSerializer
