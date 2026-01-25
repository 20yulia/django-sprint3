from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

TITLE_MAX_LENGTH = 256
NAME_MAX_LENGTH = 256


class PublishedModel(models.Model):
    """Абстрактная модель с общими полями публикации."""

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
        max_length=NAME_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


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
    # Категория обязательна в формах/админке (blank=False по умолчанию),
    # но при удалении категории используем SET_NULL => null=True.
    category: models.ForeignKey = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.title
