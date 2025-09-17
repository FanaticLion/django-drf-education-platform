from django.urls import path
from .views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, LessonUpdateAPIView, LessonDestroyAPIView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),          # GET список уроков
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'), # GET один урок
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'), # POST создать урок
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'), # PUT обновить
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'), # DELETE удалить
] + router.urls