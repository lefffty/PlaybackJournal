from rest_framework import viewsets
from rest_framework.response import Response

from .models import Song
from .serializers import SongListSerializer


class SongsListViewSet(
    viewsets.ViewSet
):
    def list(self, request):
        queryset = Song.objects.all()
        serializer = SongListSerializer(queryset, many=True, read_only=True)
        return Response(serializer.data)
