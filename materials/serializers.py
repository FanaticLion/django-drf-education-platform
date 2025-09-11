from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # Вложенный сериализатор для отображения уроков в составе курса
    lessons = LessonSerializer(source='lessons_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'