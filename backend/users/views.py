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
    mixins.RetrieveModelMixin
):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

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


class NewPasswordViewSet(viewsets.GenericViewSet):
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
