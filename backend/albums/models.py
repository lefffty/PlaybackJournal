from django.db import models
from django.contrib.auth import get_user_model

from .constants import ALBUM_NAME_MAX_LENGTH
from genre.models import Genre
from song.models import Song
from artist.models import Artist

User = get_user_model()


class Album(models.Model):
    name = models.CharField(
        verbose_name='Название альбома',
        blank=False,
        null=False,
        max_length=ALBUM_NAME_MAX_LENGTH,
    )
    publication_date = models.DateField(
        verbose_name='Дата публикации альбома',
        blank=True,
        null=True,
    )
    cover = models.ImageField(
        verbose_name='Обложка альбома',
        blank=False,
        null=False,
        upload_to='album_covers/',
    )
    artists = models.ManyToManyField(
        Artist,
        through='AlbumArtist',
        verbose_name='Исполнители, принявшие участие в альбоме'
    )
    genres = models.ManyToManyField(
        Genre,
        through='AlbumGenre',
        verbose_name='Жанры'
    )
    songs = models.ManyToManyField(
        Song,
        through='AlbumSong',
        verbose_name='Песни альбома'
    )

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name


class AbstractUserAlbumModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        verbose_name='Альбом',
    )


class RatedAlbum(AbstractUserAlbumModel):
    rating = models.FloatField(
        verbose_name='Оценка альбома',
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'Оценка альбома'
        verbose_name_plural = 'Оценки альбомов'

    def __str__(self) -> str:
        return f'{self.album.name},{self.user.username} - {self.rating}'


class FavouriteAlbum(AbstractUserAlbumModel):
    class Meta:
        verbose_name = 'Любимый альбом'
        verbose_name_plural = 'Любимые альбомы'

    def __str__(self) -> str:
        return f'{self.user.username} - {self.album.name}'


class ListenedAlbum(AbstractUserAlbumModel):
    class Meta:
        verbose_name = 'Прослушанный альбом'
        verbose_name_plural = 'Прослушанные альбомы'

    def __str__(self) -> str:
        return f'{self.user.username} - {self.album.name}'


class AlbumSong(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        verbose_name='Альбом',
        related_name='album_songs',
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        verbose_name='Песня',
    )

    class Meta:
        verbose_name = 'Песня с альбома'
        verbose_name_plural = 'Песни альбома'

    def __str__(self) -> str:
        return f'{self.album.name} - {self.song.name}'


class AlbumGenre(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        verbose_name='Альбом',
        related_name='album_genres',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Жанр альбома'
        verbose_name_plural = 'Жанры альбома'

    def __str__(self) -> str:
        return f'{self.album.name} - {self.genre.name}'


class AlbumArtist(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        verbose_name='Альбом',
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        verbose_name='Артист',
        related_name='album_artists',
    )

    class Meta:
        verbose_name = 'Автор альбома'
        verbose_name_plural = 'Авторы альбома'

    def __str__(self) -> str:
        return f'{self.artist.username} - {self.album.name}'
