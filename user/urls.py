from user.apps import UserConfig
from user.views import PaymentsListAPIView
from django.urls import path

app_name = UserConfig.name


urlpatterns = [
    path('view/', PaymentsListAPIView.as_view(), name='lesson_view'),
]