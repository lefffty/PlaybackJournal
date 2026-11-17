from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from django.http import HttpRequest
from django.db.models import Model

from .constants import RatedSongConsts
from .models import Song, RatedSong
from .serializers import (
    SongListSerializer,
    SongSerializer
)


class SongsViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = Song.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ('list',):
            return SongListSerializer
        return SongSerializer

    def get_permissions(self):
        if self.action in ("rated",):
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(
        detail=True,
        methods=['POST'],
        url_path='rated'
    )
    def rated(self, request: HttpRequest, pk: int):
        return self._set_rating(
            request,
            pk,
            RatedSong,
        )

    def _set_rating(self, request: HttpRequest, pk: int, model: Model):
        try:
            rating = int(request.data.get('rating'))
        except (ValueError, TypeError):
            return Response(
                {"detail": "Некорректный формат оценки"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not (RatedSongConsts.MIN_RATING <= rating <= RatedSongConsts.MAX_RATING):
            return Response(
                {
                    'detail': 'Оценка должна быть в диапазоне от {} до {}'.format(
                        RatedSongConsts.MIN_RATING,
                        RatedSongConsts.MAX_RATING,
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        song = self.get_object()

        filter_kwargs = {
            'user': request.user,
            'song': song,
        }

        instance = model.objects.filter(**filter_kwargs).first()

        if instance:
            old_rating = instance.rating

            if old_rating == rating:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            instance.rating = rating
            instance.save(update_fields=['rating'])
            return Response(
                {"rating": rating},
                status=status.HTTP_200_OK
            )
        filter_kwargs['rating'] = rating
        model.objects.create(**filter_kwargs)
        return Response(status=status.HTTP_201_CREATED)
