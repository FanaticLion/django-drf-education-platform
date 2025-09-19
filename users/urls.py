from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PaymentViewSet, UserViewSet
from .views import UserRegistrationAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = SimpleRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('payments/create-stripe/', PaymentViewSet.as_view({'post': 'create_stripe_payment'}), name='create-stripe-payment'),
    path('', include(router.urls)),
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]