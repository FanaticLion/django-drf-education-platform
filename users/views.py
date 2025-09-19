from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Payment, User
from .serializers import PaymentSerializer, UserProfileSerializer
from .filters import PaymentFilter
from .permissions import IsOwner
from rest_framework.decorators import action
from .stripe_service import get_stripe_session_status

try:
    from materials.models import Course, Lesson  # Модели из приложения materials
    from .stripe_service import create_stripe_product, create_stripe_price, create_stripe_checkout_session
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def check_status(self, request, pk=None):
        """Проверка статуса оплаты платежа"""
        payment = self.get_object()

        if not payment.stripe_session_id:
            return Response({"error": "У этого платежа нет сессии Stripe"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Получаем статус из Stripe
            stripe_status = get_stripe_session_status(payment.stripe_session_id)

            if stripe_status is None:
                return Response({"error": "Не удалось получить статус от Stripe"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Обновляем статус в нашей базе
            payment.stripe_payment_status = stripe_status
            payment.save()

            return Response({
                "payment_id": payment.id,
                "stripe_session_id": payment.stripe_session_id,
                "status": stripe_status,
                "amount": payment.amount,
                "item": str(payment.paid_course or payment.paid_lesson)
            })

        except Exception as e:
            return Response({"error": f"Ошибка при запросе к Stripe: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def create_stripe_payment(self, request):
        """Создание оплаты через Stripe"""
        if not STRIPE_AVAILABLE:
            return Response({"error": "Stripe не настроен"}, status=status.HTTP_501_NOT_IMPLEMENTED)

        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')

        if course_id:
            item = get_object_or_404(Course, id=course_id)
            amount = item.amount
            name = item.title
        elif lesson_id:
            item = get_object_or_404(Lesson, id=lesson_id)
            amount = item.amount
            name = item.title
        else:
            return Response({"error": "Необходимо указать course_id или lesson_id"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Создаем продукт и цену в Stripe
            product_id = create_stripe_product(name, f"Оплата {name}")
            price_id = create_stripe_price(product_id, amount)

            # Создаем сессию оплаты
            success_url = f"{settings.BASE_URL}/payment/success/"
            cancel_url = f"{settings.BASE_URL}/payment/cancel/"
            payment_url, session_id = create_stripe_checkout_session(price_id, success_url, cancel_url)

            # Сохраняем платеж в базе
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                payment_method='stripe',
                stripe_session_id=session_id,
                paid_course=item if course_id else None,
                paid_lesson=item if lesson_id else None
            )

            return Response({
                "payment_url": payment_url,
                "session_id": session_id,
                "payment_id": payment.id
            })

        except Exception as e:
            return Response({"error": f"Ошибка Stripe: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            email=serializer.validated_data['email'],
            password=request.data.get('password'),
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
            phone=serializer.validated_data.get('phone', ''),
            city=serializer.validated_data.get('city', ''),
        )

        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)