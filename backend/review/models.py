from django.db import models
from django.contrib.auth import get_user_model
import reprlib

from albums.models import Album

User = get_user_model()


class Review(models.Model):
    class ReviewType(models.TextChoices):
        POSITIVE = 'Положительная'
        NEGATIVE = 'Негативная'
        NEUTRAL = 'Нейтральная'

    title = models.CharField(
        verbose_name='Заголовок рецензии',
        max_length=128,
        null=False,
        blank=False,
    )
    text = models.TextField(
        verbose_name='Текст рецензии',
        null=False,
        blank=True,
    )
    type = models.CharField(
        verbose_name='Тип рецензии',
        null=False,
        choices=ReviewType.choices,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецензии',
        related_name='reviews',
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        verbose_name='Рецензируемый альбом',
        related_name='reviews',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата и время создания рецензии',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата и время последнего обновления рецензии',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'

    def __str__(self):
        representation = '{} - {} - {}'
        return representation.format(
            self.author.username,
            self.album.name,
            reprlib.repr(self.text)
        )
