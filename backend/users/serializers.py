from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from djoser.serializers import UserCreateSerializer, SetPasswordSerializer
from drf_extra_fields.fields import Base64ImageField

from albums.models import (
    FavouriteAlbum,
    ListenedAlbum,
    RatedAlbum,
)
from albums.serializers import (
    AlbumSimpleSerializer
)

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField(validators=[UnicodeUsernameValidator()])

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        extra_kwargs = {
            'username': {
                'required': True,
            },
            'first_name': {
                'required': True,
            },
            'last_name': {
                'required': True,
            },
            'email': {
                'required': True,
            },
            'password': {
                'required': True,
            },
        }


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'registration_date',
            'avatar',
        )


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = (
            'avatar',
        )
        extra_kwargs = {
            'avatar': {
                'required': True,
            }
        }


class NewPasswordSerializer(SetPasswordSerializer):
    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user


class UserFavouriteAlbumsSerialzer(serializers.ModelSerializer):
    album = AlbumSimpleSerializer(read_only=True)

    class Meta:
        model = FavouriteAlbum
        fields = (
            'album',
        )


class UserRatedAlbumsSerializer(serializers.ModelSerializer):
    album = AlbumSimpleSerializer(read_only=True)

    class Meta:
        model = RatedAlbum
        fields = (
            'album',
            'rating',
        )


class UserListenedAlbumsSerializer(serializers.ModelSerializer):
    album = AlbumSimpleSerializer(read_only=True)

    class Meta:
        model = ListenedAlbum
        fields = (
            'album',
        )


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )
