from rest_framework import viewsets, permissions, mixins, status
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.db.models import Model

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
    ReviewUserVote,
    ReviewComment,
    CommentUserVote,
)


class ReviewModelViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Review.objects.select_related("album", "author")

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
    def comments(self, request, pk: int):
        review = self.get_object()
        comments = review.comments.prefetch_related("author")
        serializer = ReviewCommentSerializer(
            comments, many=True, read_only=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewCommentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create',):
            return ReviewCommentCreateSerializer

    def perform_create(self, serializer: Serializer):
        serializer.save(author=self.request.user)


class ReactionViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated]

    def _toggle_reaction(
        self,
        request: HttpRequest,
        pk: int,
        _Model: Model,
        _RelatedModel: Model,
        field_name: str
    ):
        user = request.user
        obj = get_object_or_404(_Model, pk=pk)

        filter_kwargs = {
            'user': user,
            field_name: obj
        }

        instance = _RelatedModel.objects.filter(**filter_kwargs).first()
        new_reaction = request.data.get('reaction')

        if not new_reaction:
            return Response(
                "Некорректная реакция",
                status=status.HTTP_400_BAD_REQUEST
            )

        if instance:
            old_reaction = instance.reaction
            if new_reaction == old_reaction:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            instance.reaction = new_reaction
            instance.save(update_fields=['reaction'])
            return Response(
                {"reaction": new_reaction},
                status=status.HTTP_200_OK
            )
        filter_kwargs['reaction'] = new_reaction
        _RelatedModel.objects.create(**filter_kwargs)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'], url_path='review')
    def review(self, request: HttpRequest, pk: int):
        return self._toggle_reaction(
            request,
            pk,
            Review,
            ReviewUserVote,
            "review",
        )

    @action(detail=True, methods=['POST'], url_path='comment')
    def comment(self, request: HttpRequest, pk: int):
        return self._toggle_reaction(
            request,
            pk,
            ReviewComment,
            CommentUserVote,
            "comment"
        )
