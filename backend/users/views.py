from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django.http import HttpRequest

from .serializers import (
    UserCreateSerializer,
    UserProfileSerializer,
    AvatarSerializer,
    NewPasswordSerializer,
    UserRatedAlbumsSerializer,
    UserListenedAlbumsSerializer,
    UserFavouriteAlbumsSerialzer,
)
from albums.models import (
    FavouriteAlbum,
    ListenedAlbum,
    RatedAlbum,
)

User = get_user_model()


class UserCreateViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class UserProfileViewSet(
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path='me')
    def profile(self, request):
        """
        """
        serializer = UserProfileSerializer(
            request.user
        )
        return Response(serializer.data)


class AvatarViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['PUT', 'DELETE'], url_path='me/avatar')
    def avatar(self, request: HttpRequest):
        if request.method == 'PUT':
            serializer = AvatarSerializer(
                request.user,
                data=request.data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={
                    'avatar': serializer.data['avatar'],
                }
            )
        request.user.avatar.delete(save=True)
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class NewPasswordViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='set_password')
    def set_password(self, request):
        serializer = NewPasswordSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class UserAlbumsListsViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    def _get_albums_list(self, request, model, serializer):
        user = request.user
        objects = model.objects.filter(
            user=user,
        )
        _serializer = serializer(objects, many=True)
        return Response(
            _serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['GET'], url_path='favorite/albums')
    def favourite(self, request):
        return self._get_albums_list(
            request,
            FavouriteAlbum,
            UserFavouriteAlbumsSerialzer,
        )

    @action(detail=False, methods=['GET'], url_path='listened/albums')
    def listened(self, request):
        return self._get_albums_list(
            request,
            ListenedAlbum,
            UserListenedAlbumsSerializer,
        )

    @action(detail=False, methods=['GET'], url_path='rated/albums')
    def rated(self, request):
        return self._get_albums_list(
            request,
            RatedAlbum,
            UserRatedAlbumsSerializer,
        )
