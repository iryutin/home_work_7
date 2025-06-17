from django.contrib.auth.models import AbstractUser

from django.db import models

class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Укажи почту')
    phone = models.CharField(max_length=12, blank=True, null=True, verbose_name='Телефон', help_text='Укажи телефон')
    city = models.CharField()
    avatar = models.ImageField(blank=True, null=True, upload_to='user/avatars')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"