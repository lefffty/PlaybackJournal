from django.db import models
from django.contrib.auth import get_user_model

from .constants import (
    PLAYLIST_DESCRIPTION_MAX_LENGTH,
    PLAYLIST_NAME_MAX_LENGTH,
)
from song.models import Song

User = get_user_model()


class Playlist(models.Model):
    name = models.CharField(
        verbose_name='Название плейлиста',
        blank=False,
        null=False,
        max_length=PLAYLIST_NAME_MAX_LENGTH,
    )
    description = models.TextField(
        verbose_name='Описание плейлиста',
        null=True,
        blank=True,
        max_length=PLAYLIST_DESCRIPTION_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        verbose_name='Плейлист',
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        verbose_name='Песня',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор плейлиста',
    )

    class Meta:
        verbose_name = 'Песня плейлиста'
        verbose_name_plural = 'Песни плейлиста'

    def __str__(self) -> str:
        return f'Песни плейлиста {self.playlist.name}'
