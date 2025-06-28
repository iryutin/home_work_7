from django.shortcuts import render
from rest_framework import  generics
from user.models import Payments
from user.serliazers import PaymentsSerializer
from django_filters.rest_framework import DjangoFilterBackend

class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('payment_date', 'payment_course', 'paid_lesson', 'payment_method')
