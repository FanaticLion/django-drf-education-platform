from rest_framework import viewsets
from django_filters import rest_framework as filters
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']