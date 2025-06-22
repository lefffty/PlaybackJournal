from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from .serializers import GenreSerializer
from .models import Genre


class GenreListDetailViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
