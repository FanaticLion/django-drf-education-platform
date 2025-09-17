from django_filters import rest_framework as filters
from .models import Payment


class PaymentFilter(filters.FilterSet):
    #ordering = filters.OrderingFilter(
        #fields=(
            #('payment_date', 'payment_date'),
        #),
    #)

    class Meta:
        model = Payment
        fields = {
            'paid_course': ['exact'],
            'paid_lesson': ['exact'],
            'payment_method': ['exact'],
        }