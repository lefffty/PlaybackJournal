from rest_framework import serializers

from .models import Review, ReviewComment, ReviewUserVote, CommentUserVote


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
        request = self.context.get('request')
        if not request:
            return ''
        user = request.user
        if not user.is_authenticated:
            return ''
        filter_kwargs = {
            'user': user,
            'comment': obj
        }
        instance = CommentUserVote.objects.filter(**filter_kwargs)
        if instance.exists():
            return instance[0].reaction
        return ''

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
        request = self.context.get('request')
        if not request:
            return ''
        user = request.user
        if not user.is_authenticated:
            return ''
        filter_kwargs = {
            'user': user,
            'review': obj
        }
        instance = ReviewUserVote.objects.filter(**filter_kwargs)
        if instance.exists():
            return instance[0].reaction
        return ''

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
            'useful_count',
            'not_useful_count',
            'updated_at',
        )

    def get_reaction(self, obj: Review):
        request = self.context.get('request')
        if not request:
            return ''
        user = request.user
        if not user.is_authenticated:
            return ''
        filter_kwargs = {
            'user': user,
            'review': obj
        }
        instance = ReviewUserVote.objects.filter(**filter_kwargs)
        if instance.exists():
            return instance[0].reaction
        return ''

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
