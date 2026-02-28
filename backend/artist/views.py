from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from .serializers import (
    ArtistSerializer,
    ArtistSimpleSerializer
)
from .models import Artist


class ArtistViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = Artist.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ('retrieve'):
            return ArtistSerializer
        return ArtistSimpleSerializer
