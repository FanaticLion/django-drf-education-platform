import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver

def check_url_exists(url_path):
    resolver = get_resolver()
    try:
        result = resolver.resolve(url_path)
        print(f"✓ URL найден: {url_path}")
        print(f"  View: {result.func}")
        print(f"  URL name: {result.url_name}")
        print(f"  Args: {result.args}, Kwargs: {result.kwargs}")
        return True
    except Exception as e:
        print(f"✗ URL не найден: {url_path}")
        print(f"  Ошибка: {e}")
        return False

# Проверяем наш URL
check_url_exists('/api/users/payments/create-stripe/')