from django.contrib import admin
from .models import Course, Lesson, Subscription  # ДОБАВЬТЕ Subscription
from django.utils.translation import gettext_lazy as _

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    list_filter = ('title',)
    search_fields = ('title', 'description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'video_link')
    list_filter = ('course',)
    search_fields = ('title', 'description')
    raw_id_fields = ('course',)

# ДОБАВЬТЕ ЭТОТ КОД:
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'subscribed_at', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('user__email', 'course__title')
    list_editable = ('is_active',)  # Можно редактировать активность прямо в списке