Django Educational Platform
===========================

Платформа для онлайн-образования с курсами, уроками и системой платежей.

Особенности
-----------

🔐 JWT аутентификация

👥 Ролевая модель (пользователи, модераторы)

📚 Управление курсами и уроками

💳 Система платежей

🛡 Права доступа на уровне объектов

Быстрый старт

Установка зависимостей::
------------------------
poetry install

Настройка базы данных
---------------------
text
python manage.py migrate
Создание суперпользователя::

text
python manage.py createsuperuser
Запуск сервера::

text
python manage.py runserver
Структура проекта

::

text
config/
├── settings.py      # Настройки проекта
├── urls.py         # Главные URL
└── wsgi.py         # WSGI конфигурация

users/
├── models.py       # Модели User и Payment
├── serializers.py  # Сериализаторы
├── views.py        # ViewSet для пользователей и платежей
└── urls.py         # API endpoints

materials/
├── models.py       # Модели Course и Lesson
├── serializers.py  # Сериализаторы
├── views.py        # ViewSet для курсов и уроков
└── urls.py         # API endpoints
API Endpoints

Аутентификация:
---------------
POST /api/token/ - Получить JWT токен

POST /api/token/refresh/ - Обновить токен

POST /api/users/register/ - Регистрация пользователя

Пользователи:
-------------
GET /api/users/ - Список пользователей

GET /api/users/{id}/ - Профиль пользователя

PUT /api/users/{id}/ - Обновление профиля

Курсы:
------

GET /api/courses/ - Список курсов

POST /api/courses/ - Создать курс

GET /api/courses/{id}/ - Детали курса

PUT /api/courses/{id}/ - Обновить курс

DELETE /api/courses/{id}/ - Удалить курс

Уроки:
------

GET /api/lessons/ - Список уроков

POST /api/lessons/create/ - Создать урок

GET /api/lessons/{id}/ - Детали урока

PUT /api/lessons/{id}/update/ - Обновить урок

DELETE /api/lessons/{id}/delete/ - Удалить урок

Платежи:
--------

GET /api/payments/ - История платежей

POST /api/payments/ - Создать платеж

Права доступа

Модераторы:
-----------
✅ Просмотр всех курсов и уроков

✅ Редактирование любых курсов и уроков

❌ Создание курсов и уроков

❌ Удаление курсов и уроков

Обычные пользователи:
^^^^^^^^^^^^^^^^^^^^

✅ Просмотр только своих материалов

✅ Создание своих курсов и уроков

✅ Редактирование только своих материалов

✅ Удаление только своих материалов

Модели
------
User
^^^^
.. code-block:: python

text
class User(AbstractUser):
    # email вместо username
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='users/avatars/')
Course
^^^^^^
.. code-block:: python

text
class Course(models.Model):
    title = models.CharField(max_length=150)
    preview = models.ImageField(upload_to='courses/previews/')
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL)
Lesson
^^^^^^
.. code-block:: python

text
class Lesson(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    preview = models.ImageField(upload_to='lessons/previews/')
    video_link = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL)
Payment
^^^^^^^
.. code-block:: python

text
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10)
Разработка

Тестирование::
###
text
python manage.py test
Создание миграций::

text
python manage.py makemigrations
Запуск тестового сервера::

text
python manage.py runserver 0.0.0.0:8000
Лицензия

MIT License

Авторы
#####
Денис шевченко 
den20020805@gmail.com

Этот файл README.rst содержит:

📋 Описание проекта

🚀 Инструкции по установке

🔗 API endpoints

🛡 Систему прав доступа

📊 Описание моделей

🛠 Команды для разработки