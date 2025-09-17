from rest_framework import serializers
from .models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'payments')
        extra_kwargs = {
            'password': {'write_only': True},
            'last_name': {'write_only': True}  # скрываем фамилию при чтении
        }

    def to_representation(self, instance):
        """Скрываем конфиденциальные данные при просмотре чужого профиля"""
        representation = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.user != instance:
            # Для чужого профиля скрываем чувствительные данные
            representation.pop('phone', None)
            representation.pop('city', None)
            representation.pop('payments', None)

        return representation