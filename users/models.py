from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager  # Менеджер создадим ниже


class User(AbstractUser):
    # Убираем поле username, делаем email уникальным идентификатором
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # Добавляем новые поля
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватарка')

    # Указываем, что поле email используется для входа
    USERNAME_FIELD = 'email'
    # Поля, которые обязательны для создания суперпользователя (email и так обязателен из-за USERNAME_FIELD)
    REQUIRED_FIELDS = []

    # Подключаем кастомный менеджер для обработки создания пользователей
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email