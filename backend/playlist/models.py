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
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор плейлиста',
        related_name='user_playlists'
    )
    songs = models.ManyToManyField(
        Song,
        through='PlaylistSong',
        verbose_name='Песни в плейлисте',
    )
    cover = models.ImageField(
        verbose_name='Аватар плейлиста',
        upload_to='playlists_avatars/',
        default='default_images/default playlist cover.jpg',
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
        verbose_name='Название плейлиста',
        related_name='playlist_songs',
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        verbose_name='Название песни',
    )

    class Meta:
        verbose_name = 'Песня плейлиста'
        verbose_name_plural = 'Песни плейлиста'
        ordering = ('id',)

    def __str__(self) -> str:
        return f'{self.playlist.name} - {self.song.name}'
