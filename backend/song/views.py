from rest_framework import (
    viewsets,
    mixins,
    permissions,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpRequest
from django.db.models import Model

from .models import Song, RatedSong
from .serializers import (
    SongListSerializer,
    SongSerializer
)


class SongsListRetrieveViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = Song.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ('list'):
            return SongListSerializer
        return SongSerializer


class UserSongPreferencesViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated]

    def _create_user_song_item(self, request: HttpRequest, pk: int, model: Model):
        filter_kwargs = {
            'user': request.user,
            'song': Song.objects.get(pk=pk),
        }
        instance = model.objects.filter(**filter_kwargs)
        rating = request.data.get('rating')
        if instance.exists():
            if rating is None:
                pass
            if not (0 <= rating <= 10):
                pass
            instance.update(rating=rating)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            filter_kwargs['rating'] = rating
            model.objects.create(**filter_kwargs)
            return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST'],
        url_path='rated'
    )
    def rated_song(self, request: HttpRequest, pk: int):
        return self._create_user_song_item(
            request,
            pk,
            RatedSong,
        )
