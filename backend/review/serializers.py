from rest_framework import serializers

from users.serializers import UserSimpleSerializer
from .models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            'title',
            'text',
            'type',
            'author',
            'updated_at',
        )


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
