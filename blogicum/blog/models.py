from __future__ import annotations

from typing import ClassVar

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()

TITLE_MAX_LENGTH: int = 256
SLUG_MAX_LENGTH: int = 64


class PublishedModel(models.Model):
    """Абстрактная модель с флагом публикации и датой создания."""

    is_published: models.BooleanField = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at: models.DateTimeField = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Category(PublishedModel):
    title: models.CharField = models.CharField(
        'Заголовок',
        max_length=TITLE_MAX_LENGTH,
    )
    description: models.TextField = models.TextField('Описание')
    slug: models.SlugField = models.SlugField(
        'Идентификатор',
        max_length=SLUG_MAX_LENGTH,
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Location(PublishedModel):
    name: models.CharField = models.CharField(
        'Название места',
        max_length=TITLE_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class PostQuerySet(models.QuerySet['Post']):
    def published(self) -> models.QuerySet['Post']:
        """Опубликованные посты с датой публикации не в будущем."""
        return self.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
        )


class Post(PublishedModel):
    title: models.CharField = models.CharField(
        'Заголовок',
        max_length=TITLE_MAX_LENGTH,
    )
    text: models.TextField = models.TextField('Текст')
    pub_date: models.DateTimeField = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
        default=timezone.now,
    )
    author: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location: models.ForeignKey = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
    )
    # ВАЖНО: blank не задаём → blank=False по умолчанию.
    # Это то, что требуют тесты по атрибуту category.
    category: models.ForeignKey = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )

    objects: ClassVar[models.Manager['Post']] = PostQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.title
