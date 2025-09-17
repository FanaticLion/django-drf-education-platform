from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import Group
from users.models import User
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_only


class MaterialsTestCase(APITestCase):

    def setUp(self):
        # Создаем группы
        self.moderator_group, _ = Group.objects.get_or_create(name='moderators')

        # Создаем пользователей
        self.user1 = User.objects.create_user(
            email='user1@test.com', password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com', password='testpass123'
        )
        self.moderator = User.objects.create_user(
            email='moderator@test.com', password='testpass123'
        )
        self.moderator.groups.add(self.moderator_group)

        # Создаем курсы и уроки
        self.course1 = Course.objects.create(
            title='Курс 1', description='Описание 1', owner=self.user1
        )
        self.course2 = Course.objects.create(
            title='Курс 2', description='Описание 2', owner=self.user2
        )

        self.lesson1 = Lesson.objects.create(
            title='Урок 1', description='Описание урока 1',
            video_link='https://youtube.com/watch?v=test1', owner=self.user1, course=self.course1
        )
        self.lesson2 = Lesson.objects.create(
            title='Урок 2', description='Описание урока 2',
            video_link='https://youtu.be/test2', owner=self.user2, course=self.course2
        )

        # Клиенты для разных пользователей
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.client_moderator = APIClient()

        self.client1.force_authenticate(user=self.user1)
        self.client2.force_authenticate(user=self.user2)
        self.client_moderator.force_authenticate(user=self.moderator)

    def test_youtube_validator(self):
        """Тест валидатора YouTube ссылок"""
        # Правильные ссылки
        self.assertEqual(validate_youtube_only('https://youtube.com/watch?v=test'), 'https://youtube.com/watch?v=test')
        self.assertEqual(validate_youtube_only('https://www.youtube.com/watch?v=test'),
                         'https://www.youtube.com/watch?v=test')
        self.assertEqual(validate_youtube_only('https://youtu.be/test'), 'https://youtu.be/test')

        # Неправильные ссылки
        with self.assertRaises(Exception):
            validate_youtube_only('https://vk.com/video/test')
        with self.assertRaises(Exception):
            validate_youtube_only('https://rutube.ru/video/test')

    def test_lesson_create_with_valid_link(self):
        """Тест создания урока с валидной YouTube ссылкой"""
        url = reverse('lesson-create')
        data = {
            'title': 'Новый урок',
            'description': 'Описание',
            'video_link': 'https://youtube.com/watch?v=abc123',
            'course': self.course1.id
        }
        response = self.client1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_create_with_invalid_link(self):
        """Тест создания урока с невалидной ссылкой"""
        url = reverse('lesson-create')
        data = {
            'title': 'Новый урок',
            'description': 'Описание',
            'video_link': 'https://vk.com/video/test',
            'course': self.course1.id
        }
        response = self.client1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscription_flow(self):
        """Тест работы подписок"""
        url = reverse('subscription')

        # Добавление подписки
        response = self.client1.post(url, {'course_id': self.course1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user1, course=self.course1).exists())

        # Удаление подписки
        response = self.client1.post(url, {'course_id': self.course1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user1, course=self.course1).exists())

    def test_course_list_with_subscription_flag(self):
        """Тест отображения флага подписки в курсах"""
        # Добавляем подписку
        Subscription.objects.create(user=self.user1, course=self.course1)

        url = reverse('course-list')
        response = self.client1.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course_data = response.data['results'][0]  # Для пагинации
        self.assertTrue(course_data['is_subscribed'])  # Должен быть True

    def test_permissions_lesson_access(self):
        """Тест прав доступа к урокам"""
        url = reverse('lesson-detail', kwargs={'pk': self.lesson2.id})

        # user1 не должен видеть урок user2
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Модератор должен видеть все уроки
        response = self.client_moderator.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination(self):
        """Тест пагинации"""
        # Создаем больше уроков для теста пагинации
        for i in range(15):
            Lesson.objects.create(
                title=f'Урок {i + 3}',
                description=f'Описание {i + 3}',
                video_link=f'https://youtube.com/watch?v=test{i + 3}',
                owner=self.user1,
                course=self.course1
            )

        url = reverse('lesson-list')
        response = self.client1.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 10)  # page_size


class SubscriptionModelTest(TestCase):
    def test_unique_subscription(self):
        """Тест уникальности подписки"""
        user = User.objects.create_user(email='test@test.com', password='testpass')
        course = Course.objects.create(title='Тестовый курс', description='Описание', owner=user)

        # Первая подписка
        Subscription.objects.create(user=user, course=course)

        # Вторая подписка должна вызвать ошибку
        with self.assertRaises(Exception):
            Subscription.objects.create(user=user, course=course)