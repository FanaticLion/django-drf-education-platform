from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
#from materials.models import Course, Subscription
#from users.models import User


@shared_task
def send_course_update_notification(course_id):
    """
    Асинхронная отправка уведомлений об обновлении курса
    """
    # Импорты внутри функции
    from materials.models import Course, Subscription
    from users.models import User

    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course, is_active=True)

        for subscription in subscriptions:
            user = subscription.user
            subject = f'Обновление курса: {course.title}'
            message = f'Курс "{course.title}" был обновлен. Проверьте новые материалы!'

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

        return f'Уведомления отправлены для курса {course.title} ({subscriptions.count()} подписчиков)'
    except Course.DoesNotExist:
        return f'Курс с id {course_id} не найден'


@shared_task
def deactivate_inactive_users():
    """
    Периодическая задача: блокировка пользователей, не заходивших более месяца
    """
    # Импорты внутри функции
    from users.models import User
    from django.utils import timezone
    from datetime import timedelta

    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True
    )

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    return f'Заблокировано {count} неактивных пользователей'