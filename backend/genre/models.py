from django.db import models
from django.contrib.auth import get_user_model

from .constants import (
    GENRE_DESCRIPTION_MAX_LENGTH,
    GENRE_NAME_MAX_LENGTH,
)

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        blank=False,
        null=False,
        max_length=GENRE_NAME_MAX_LENGTH,
        unique=True,
    )
    description = models.CharField(
        verbose_name='Краткое описание жанра',
        blank=True,
        null=False,
        max_length=GENRE_DESCRIPTION_MAX_LENGTH,
    )
    albums = models.ManyToManyField(
        'albums.Album',
        through='albums.AlbumGenre',
    )
    artists = models.ManyToManyField(
        'artist.Artist',
        through='artist.ArtistGenre',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)

    def __str__(self):
        return self.name


class FavouriteGenre(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_favourite_genres',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Любимый жанр'
        verbose_name_plural = 'Любимые жанры'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'genre'],
                name='unique_%(class)s'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.genre.name}'
