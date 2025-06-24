from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from .serializers import ArtistSerializer
from .models import Artist


class ArtistViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = Artist.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ArtistSerializer
    pagination_class = LimitOffsetPagination
