from __future__ import annotations
from django.db import models
from django.contrib.auth import get_user_model
import reprlib

from albums.models import Album

User = get_user_model()


class Review(models.Model):
    class ReviewType(models.TextChoices):
        POSITIVE = 'positive'
        NEGATIVE = 'negative'
        NEUTRAL = 'neutral'

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


class ReviewComment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария',
        null=False,
        blank=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемая рецензия',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата и время написания комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий к рецензии'
        verbose_name_plural = 'Комментарии к рецензии'

    @property
    def plus_count(self):
        return self.reactions.filter(reaction=CommentUserVote.ReviewReaction.PLUS).count()

    @property
    def minus_count(self):
        return self.reactions.filter(reaction=CommentUserVote.ReviewReaction.MINUS).count()

    def __str__(self):
        representation = '{} - {} - {}'
        return representation.format(
            self.author.username,
            self.review.title,
            reprlib.repr(self.text)
        )


class ReviewUserVote(models.Model):
    class ReviewReaction(models.TextChoices):
        USEFUL = 'useful',
        NOT_USEFUL = 'not_useful',

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Рецензия',
        related_name='reactions',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    reaction = models.CharField(
        max_length=20,
        verbose_name='Реакция на рецензию',
        choices=ReviewReaction.choices
    )

    class Meta:
        verbose_name = 'Реакция на рецензию'
        verbose_name_plural = 'Реакции на рецензию'
        constraints = [
            models.UniqueConstraint(
                fields=['review', 'user'],
                name='unique_%(class)s'
            )
        ]


class CommentUserVote(models.Model):
    class ReviewReaction(models.TextChoices):
        MINUS = 'minus'
        PLUS = 'plus'

    comment = models.ForeignKey(
        ReviewComment,
        on_delete=models.CASCADE,
        verbose_name='Комментарий',
        related_name='reactions',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    reaction = models.CharField(
        max_length=20,
        choices=ReviewReaction.choices,
        verbose_name='Реакция на комментарий'
    )

    class Meta:
        verbose_name = 'Реакция на комментарий'
        verbose_name_plural = 'Реакции на комментарий'
        constraints = [
            models.UniqueConstraint(
                fields=['comment', 'user'],
                name='unique_%(class)s',
            )
        ]
