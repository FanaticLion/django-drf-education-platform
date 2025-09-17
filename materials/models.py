from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/previews/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
    null=True, blank=True, verbose_name='Владелец')


class Meta:
    verbose_name = 'Курс'
    verbose_name_plural = 'Курсы'


def __str__(self):
    return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    preview = models.ImageField(upload_to='lessons/previews/', blank=True, null=True, verbose_name='Превью')
    video_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
    null=True, blank=True, verbose_name='Владелец')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='lessons', blank=True, null=True,
    verbose_name='Курс')


class Meta:
    verbose_name = 'Урок'
    verbose_name_plural = 'Уроки'


def __str__(self):
    return self.title


class Subscription(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'course']  # Одна подписка на пользователя и курс

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"