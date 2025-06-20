from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model

from .serializers import (
    UserCreateSerializer,
    UserListDetailSerializer
)

User = get_user_model()


class UserCreateListViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserListDetailSerializer
