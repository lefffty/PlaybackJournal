from rest_framework import viewsets, permissions, mixins
from rest_framework.serializers import Serializer

from .serializers import (
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
    ReviewDetailSerializer,
    ReviewCommentCreateSerializer
)
from .permissions import IsOwnerOrReadOnly
from .models import (
    Review,
)


class ReviewModelViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action in ('create',):
            return ReviewCreateSerializer
        elif self.action in ('retrieve',):
            return ReviewDetailSerializer
        else:
            return ReviewUpdateSerializer

    def get_permissions(self):
        if self.action in ('create',):
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer: Serializer):
        serializer.save(author=self.request.user)


class ReviewCommentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', ):
            return ReviewCommentCreateSerializer

    def perform_create(self, serializer: Serializer):
        serializer.save(author=self.request.user)
