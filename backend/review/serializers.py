from rest_framework import serializers

from .models import Review, ReviewComment


class ReviewCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = (
            'text',
            'review',
        )


class ReviewCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = ReviewComment
        fields = (
            'text',
            'author',
            'created_at',
        )

    def get_author(self, obj: ReviewComment):
        from users.serializers import UserSimpleSerializer
        serializer = UserSimpleSerializer(obj.author)
        return serializer.data


class ReviewListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'text',
            'type',
            'author',
            'updated_at',
        )

    def get_author(self, obj: Review):
        from users.serializers import UserSimpleSerializer
        author = obj.author
        serializer = UserSimpleSerializer(author)
        return serializer.data


class ReviewDetailSerializer(serializers.ModelSerializer):
    comments = ReviewCommentSerializer(read_only=True, many=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'text',
            'type',
            'author',
            'updated_at',
            'comments',
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
