from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/previews/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              null=True, blank=True, verbose_name='Владелец')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость курса')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    def save(self, *args, **kwargs):
        if self.pk:
            from .tasks import send_course_update_notification

            old_course = Course.objects.get(pk=self.pk)
            four_hours_ago = timezone.now() - timedelta(hours=4)  # ← 4 ЧАСА!

            print(f"=== SAVE METHOD CALLED ===")
            print(f"Old updated_at: {old_course.updated_at}")
            print(f"Four hours ago: {four_hours_ago}")

            if old_course.updated_at < four_hours_ago:
                send_course_update_notification.delay(self.id)
                print("=== TASK SENT ===")

        super().save(*args, **kwargs)

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
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость урока')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'course']  # Одна подписка на пользователя и курс

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"