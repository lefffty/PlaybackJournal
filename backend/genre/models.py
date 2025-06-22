from django.db import models

from .constants import (
    GENRE_DESCRIPTION_MAX_LENGTH,
    GENRE_NAME_MAX_LENGTH,
)


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
