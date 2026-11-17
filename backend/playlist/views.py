from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.http import HttpRequest

from .serializers import (
    PlaylistSerializer,
    PlaylistDetailSerializer,
    PlaylistCreateUpdateSerializer
)
from .constants import RatedPlaylistsConsts
from .permissions import OwnerOrReadOnly
from .models import (
    Playlist,
    RatedPlaylist,
    FavouritePlaylist
)


class PlaylistViewSet(
    viewsets.ModelViewSet
):
    queryset = Playlist.objects.all()
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ("status", "rated", "favourite"):
            return [IsAuthenticated()]
        if self.action in ("list", "retrieve", "create"):
            return [IsAuthenticatedOrReadOnly()]
        return [OwnerOrReadOnly()]

    def get_serializer_class(self):
        if self.action in ('list',):
            return PlaylistSerializer
        if self.action in ('retrieve',):
            return PlaylistDetailSerializer
        return PlaylistCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        url_path='status',
    )
    def status(self, request: HttpRequest, pk: int):
        playlist = self.get_object()
        user = request.user

        rating = RatedPlaylist.objects.filter(user=user, playlist=playlist).values_list("rating", flat=True).first()

        response = {
            'favourite': FavouritePlaylist.objects.filter(user=user, playlist=playlist).exists(),
            'rating': rating or 0,
        }

        return Response(response, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST'],
        url_path='favourite'
    )
    def favourite(self, request: HttpRequest, pk: int):
        return self._toggle_item(request, pk)

    @action(
        detail=True,
        methods=['POST'],
        url_path='rated'
    )
    def rated(self, request: HttpRequest, pk: int):
        return self._set_rating(request, pk)

    def _toggle_item(self, request: HttpRequest, pk: int):
        playlist = self.get_object()
        user = request.user

        params = {
            'playlist': playlist,
            'user': user
        }

        instance = FavouritePlaylist.objects.filter(**params)

        if instance.exists():
            instance[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        FavouritePlaylist.objects.create(**params)
        return Response(status=status.HTTP_201_CREATED)

    def _set_rating(self, request: HttpRequest, pk: int):
        try:
            rating = int(request.data.get('rating'))
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Некорректный формат оценки'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (RatedPlaylistsConsts.MIN_RATING <= rating <= RatedPlaylistsConsts.MAX_RATING):
            return Response(
                {'detail': 'Оценка должна быть в диапазоне от {} до {}'.format(
                        RatedPlaylistsConsts.MIN_RATING,
                        RatedPlaylistsConsts.MAX_RATING,
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        playlist = self.get_object()
        user = request.user

        params = {
            'playlist': playlist,
            'user': user
        }

        instance = RatedPlaylist.objects.filter(**params)

        if instance.exists():
            old_rating = instance[0].rating
            if old_rating == rating:
                instance.delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            instance[0].rating = rating
            instance[0].save(update_fields=['rating'])
            return Response(
                {"rating": rating},
                status=status.HTTP_200_OK,
            )
        params['rating'] = rating
        RatedPlaylist.objects.create(**params)
        return Response(status=status.HTTP_201_CREATED)
