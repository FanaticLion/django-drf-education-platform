from django_filters import rest_framework as filters
from .models import Payment


class PaymentFilter(filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'paid_course': ['exact'],
            'paid_lesson': ['exact'],
            'payment_method': ['exact'],
        }

    ordering = filters.OrderingFilter(
        fields=(
            ('payment_date', 'date'),
        ),
    )