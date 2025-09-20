from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Course
from .tasks import send_course_update_notification

@receiver(post_save, sender=Course)
def course_update_handler(sender, instance, created, **kwargs):
    if not created:  # только при обновлении существующего курса
        four_hours_ago = timezone.now() - timedelta(hours=4)
        if instance.updated_at < four_hours_ago:
            send_course_update_notification.delay(instance.id)