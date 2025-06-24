from rest_framework import serializers

from .models import Song


class SongSerializer(serializers.ModelSerializer):
    song_name = serializers.CharField(source='name')
    song_duration = serializers.TimeField(source='duration')
    song_id = serializers.IntegerField(source='id')

    class Meta:
        model = Song
        fields = (
            'song_id',
            'song_name',
            'song_duration',
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
