from rest_framework import viewsets, permissions, mixins, status
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .serializers import (
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
    ReviewDetailSerializer,
    ReviewCommentSerializer,
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

    @action(
        detail=True,
        methods=['GET'],
        url_path='comments'
    )
    def get_review_comments(self, request, pk: int):
        review = get_object_or_404(Review, pk=pk)
        comments = review.comments.all()
        serializer = ReviewCommentSerializer(
            comments, many=True, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
