from rest_framework import serializers
from urllib.parse import urlparse


def validate_youtube_only(value):
    """Валидатор, проверяющий что ссылка ведет только на youtube.com"""
    if value:
        parsed_url = urlparse(value)
        # Проверяем, что домен - youtube.com или youtu.be
        if parsed_url.netloc not in ['youtube.com', 'www.youtube.com', 'youtu.be']:
            raise serializers.ValidationError(
                "Разрешены только ссылки на YouTube (youtube.com или youtu.be)"
            )
    return value


class YouTubeValidator:
    """Класс-валидатор для проверки YouTube ссылок"""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if value:
            parsed_url = urlparse(value)
            if parsed_url.netloc not in ['youtube.com', 'www.youtube.com', 'youtu.be']:
                raise serializers.ValidationError(
                    {self.field: "Разрешены только ссылки на YouTube"}
                )
        return attrs