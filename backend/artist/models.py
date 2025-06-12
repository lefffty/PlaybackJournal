from django.db import models

from .constants import (
    ARTIST_USERNAME_MAX_LENGTH,
    ARTIST_DESCRIPTION_MAX_LENGTH,
)
from song.models import Song
from genre.models import Genre


class Artist(models.Model):
    username = models.CharField(
        verbose_name='Имя артиста',
        blank=False,
        null=False,
        max_length=ARTIST_USERNAME_MAX_LENGTH,
        unique=True,
    )
    description = models.TextField(
        max_length=ARTIST_DESCRIPTION_MAX_LENGTH,
        verbose_name='Краткие сведения об артисте',
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to='artist_avatars/',
        verbose_name='Изображение исполнителя',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.username


class RelatedArtists(models.Model):
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        verbose_name='Артист',
        related_name='similar_artists',
    )
    related_artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        verbose_name='Похожий артист',
        related_name='similar_to_artists',
    )

    class Meta:
        verbose_name = 'Похожий исполнитель'
        verbose_name_plural = 'Похожие исполнители'
        ordering = ('id',)

    def __str__(self) -> str:
        return (f'{self.related_artist.username}'
                f' похож на {self.artist.username}')


class ArtistGenre(models.Model):
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр, в котором автор работает',
    )

    class Meta:
        verbose_name = 'Жанр автора'
        verbose_name_plural = 'Жанры авторов'

    def __str__(self) -> str:
        return (f'{self.artist.username} '
                f'играет в жанре {self.genre.name}')


class ArtistSong(models.Model):
    artist = models.ForeignKey(
        Artist,
        on_delete=models.DO_NOTHING,
        verbose_name='Исполнитель'
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.DO_NOTHING,
        verbose_name='Песня',
    )

    class Meta:
        verbose_name = 'Исполнитель песни'
        verbose_name_plural = 'Исполнители песни'

    def __str__(self) -> str:
        return f'{self.artist.username} исполнитель песни {self.song.name}'
