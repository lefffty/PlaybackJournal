from rest_framework import serializers

from .models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
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
