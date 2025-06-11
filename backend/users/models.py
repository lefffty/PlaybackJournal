from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    NAME_MAX_LENGTH,
    SURNAME_MAX_LENGTH,
    USERNAME_MAX_LENGTH
)


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм пользователя',
        blank=False,
        null=False,
        unique=True,
        max_length=USERNAME_MAX_LENGTH,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        blank=False,
        null=False,
        max_length=NAME_MAX_LENGTH,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        blank=False,
        null=False,
        max_length=SURNAME_MAX_LENGTH,
    )
    email = models.EmailField(
        verbose_name='Почтовый адрес пользователя',
        blank=False,
        null=False,
        unique=True,
    )
    registration_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации пользователя',
    )
    avatar = models.ImageField(
        verbose_name='Аватар пользователя',
        blank=True,
        null=True,
        upload_to='user_avatars/',
    )

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-registration_date']

    def __str__(self):
        return self.username
