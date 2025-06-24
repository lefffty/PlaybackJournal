from django.db import models

from .constants import SONG_NAME_MAX_LENGTH


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
