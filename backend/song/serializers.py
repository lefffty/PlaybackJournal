from rest_framework import serializers

from .models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = (
            'id',
            'name',
            'duration',
        )


class SongSimpleSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all()
    )

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        return {
            'song': ret['id']
        }
