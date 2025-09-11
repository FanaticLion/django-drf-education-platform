from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView

# Настройка роутера для ViewSet
router = SimpleRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    # Маршруты для курсов (обрабатываются роутером)
    path('', include(router.urls)),

    # Маршруты для уроков (явно прописанные для Generic)
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
]