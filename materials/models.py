from django.db import models

class Rate (models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя_курса")
    image = models.ImageField(blank=True, null=True, upload_to='rate')
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя_урока")
    image = models.ImageField(blank=True, null=True, upload_to='lesson')
    description = models.TextField(blank=True, null=True)
    video = models.FileField(blank=True, null=True, upload_to='lesson/video')
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"