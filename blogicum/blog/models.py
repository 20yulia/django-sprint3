from __future__ import annotations

from typing import ClassVar

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title: models.CharField = models.CharField('Заголовок', max_length=256)
    description: models.TextField = models.TextField('Описание')

    jls_extract_var: ClassVar[str] = 'Идентификатор'
    slug: models.SlugField = models.SlugField(
        jls_extract_var,
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        ),
    )

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
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Location(models.Model):
    name: models.CharField = models.CharField('Название места', max_length=256)
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
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    title: models.CharField = models.CharField('Заголовок', max_length=256)
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
    )
    location: models.ForeignKey = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    # Категория обязательна в формах/админке (blank=False),
    # но при удалении категории используем SET_NULL => null=True
    category: models.ForeignKey = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория',
    )
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
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.title
