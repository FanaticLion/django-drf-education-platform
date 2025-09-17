from rest_framework import viewsets, generics, permissions, status  # Один импорт!
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from .models import Payment, User
from .serializers import PaymentSerializer, UserProfileSerializer
from .filters import PaymentFilter
from .permissions import IsOwner

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            # Редактировать и удалять можно только свой профиль
            self.permission_classes = [permissions.IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def get_serializer_context(self):
        """Передаем request в сериализатор"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Создаем пользователя с хешированным паролем
        user = User.objects.create_user(
            email=serializer.validated_data['email'],
            password=request.data.get('password'),  # пароль из запроса
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
            phone=serializer.validated_data.get('phone', ''),
            city=serializer.validated_data.get('city', ''),
        )

        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)