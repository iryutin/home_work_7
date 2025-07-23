from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.apps import UserConfig
from user.views import (
    PaymentCancelAPIView,
    PaymentsCreateAPIView,
    PaymentsListAPIView,
    PaymentSuccessAPIView,
    StripeCheckoutSessionAPIView,
    StripeStatusAPIView,
    UserCreateAPIView,
    SubscriptionView,
)

app_name = UserConfig.name


urlpatterns = [
    path("view/", PaymentsListAPIView.as_view(), name="lesson_view"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreateAPIView.as_view(), name="register_user"),
    path("subscriptions/", SubscriptionView.as_view(), name="subscription"),
    path(
        "stripe/checkout/",
        StripeCheckoutSessionAPIView.as_view(),
        name="stripe_checkout",
    ),
    path("payment-success/", PaymentSuccessAPIView.as_view(), name="payment_success"),
    path("payment-cancel/", PaymentCancelAPIView.as_view(), name="payment_cancel"),
    path("create-payment/", PaymentsCreateAPIView.as_view(), name="create_payment"),
    path("stripe/status/", StripeStatusAPIView.as_view(), name="stripe_status"),
]
