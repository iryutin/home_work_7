from django.shortcuts import render
from rest_framework import generics
from user.models import Payments
from user.serliazers import PaymentsSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from user.models import User, Subscription
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from materials.models import Rate
from rest_framework.response import Response
import stripe
from django.conf import settings


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        "payment_date",
        "payment_course",
        "paid_lesson",
        "payment_method",
    )


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Rate, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StripeCheckoutSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        course = Rate.objects.get(id=course_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # 1. Create product
        product = stripe.Product.create(
            name=course.name,
            description=course.description or "",
        )
        # 2. Create price
        price = stripe.Price.create(
            product=product.id,
            unit_amount=int(100 * float(request.data.get("amount", 1000))),  # amount in cents
            currency="usd",
        )
        # 3. Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price.id,
                "quantity": 1,
            }],
            mode="payment",
            success_url=request.build_absolute_uri("/user/payment-success/"),
            cancel_url=request.build_absolute_uri("/user/payment-cancel/"),
            customer_email=request.user.email,
        )
        return Response({"checkout_url": session.url})

class PaymentSuccessAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response({"status": "success", "message": "Payment successful!"})

class PaymentCancelAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response({"status": "cancelled", "message": "Payment cancelled."})