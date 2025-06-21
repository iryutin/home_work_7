from django.contrib.auth.models import AbstractUser
from materials.models import Rate, Lesson
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

class Payments(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_created=True, auto_now=True)
    payment_course = models.ForeignKey(Rate, on_delete=models.SET_NULL, null=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits = 50, decimal_places = 50)
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS,
        verbose_name='Способ оплаты'
    )
