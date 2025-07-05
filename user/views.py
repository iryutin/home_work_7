from django.shortcuts import render
from rest_framework import generics
from user.models import Payments
from user.serliazers import PaymentsSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from user.models import User
from rest_framework.permissions import AllowAny


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
