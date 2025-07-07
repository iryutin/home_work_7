from django.db import models

from django.contrib.auth import get_user_model


class Rate(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя_курса")
    image = models.ImageField(blank=True, null=True, upload_to="rate")
    description = models.TextField(blank=True, null=True)
    owner = models.OneToOneField(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя_урока")
    image = models.ImageField(blank=True, null=True, upload_to="lesson")
    description = models.TextField(blank=True, null=True)
    video = models.TextField(blank=True, null=True)
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    owner = models.OneToOneField(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
