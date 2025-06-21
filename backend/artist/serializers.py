from rest_framework import serializers

from .models import Artist


class ArtistSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'username',
            'avatar'
        )
