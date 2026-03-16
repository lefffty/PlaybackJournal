from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from .constants import SONG_NAME_MAX_LENGTH

User = get_user_model()


class Song(models.Model):
    name = models.CharField(
        verbose_name='Название песни',
        null=False,
        blank=False,
        max_length=SONG_NAME_MAX_LENGTH,
    )
    duration = models.TimeField(
        verbose_name='Длительность песни'
    )
    artists = models.ManyToManyField(
        'artist.Artist',
        through='artist.ArtistSong',
    )

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'
        ordering = ('id',)

    def __str__(self):
        return self.name


class RatedSong(models.Model):
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        verbose_name='Песня'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    rating = models.IntegerField(
        verbose_name='Оценка',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0),
        ]
    )

    class Meta:
        verbose_name = 'Оценка песни'
        verbose_name_plural = 'Оценки песен'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'song'],
                name='unique_%(class)s',
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.song.name} - {self.rating}'
