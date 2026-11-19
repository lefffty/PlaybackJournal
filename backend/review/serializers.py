from rest_framework import serializers

from .models import Review, ReviewComment, ReviewUserVote, CommentUserVote
from .utils import get_user_reaction


class ReviewCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = (
            'text',
            'review',
        )


class ReviewCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    reaction = serializers.SerializerMethodField()

    class Meta:
        model = ReviewComment
        fields = (
            'id',
            'text',
            'author',
            'created_at',
            'plus_count',
            'minus_count',
            'reaction',
        )

    def get_reaction(self, obj: ReviewComment):
        return get_user_reaction(
            self.context.get('request'),
            obj,
            CommentUserVote,
            "comment"
        )

    def get_author(self, obj: ReviewComment):
        from users.serializers import UserSimpleSerializer
        serializer = UserSimpleSerializer(obj.author)
        return serializer.data


class ReviewListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    reaction = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'text',
            'type',
            'author',
            'album',
            'useful_count',
            'not_useful_count',
            'reaction',
            'updated_at',
        )

    def get_reaction(self, obj: Review):
        return get_user_reaction(
            self.context.get('request'),
            obj,
            ReviewUserVote,
            "review"
        )

    def get_author(self, obj: Review):
        from users.serializers import UserSimpleSerializer
        author = obj.author
        serializer = UserSimpleSerializer(author)
        return serializer.data


class ReviewDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    reaction = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'text',
            'type',
            'author',
            'reaction',
            'album',
            'useful_count',
            'not_useful_count',
            'updated_at',
        )

    def get_reaction(self, obj: Review):
        return get_user_reaction(
            self.context.get('request'),
            obj,
            ReviewUserVote,
            "review"
        )

    def get_author(self, obj: Review):
        from users.serializers import UserSimpleSerializer
        author = obj.author
        serializer = UserSimpleSerializer(author)
        return serializer.data


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'title',
            'text',
            'type',
            'album',
        )


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'title',
            'text',
            'type',
        )
