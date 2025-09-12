from django.contrib import admin
from .models import Course, Lesson
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