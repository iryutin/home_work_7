from django.core.management.base import BaseCommand
from user.models import Payments
from django.contrib.auth import get_user_model
from materials.models import Rate, Lesson
from django.utils import timezone
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test users, courses, lessons and payments'

    def handle(self, *args, **options):
        # Создаем группы
        moderator_group, _ = Group.objects.get_or_create(name="moderators")
        student_group, _ = Group.objects.get_or_create(name="students")

        #Создаём админа
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="admin123",
            first_name="Admin",
            last_name="User",
        )

        # Создаем тестовых пользователей
        user1, created = User.objects.get_or_create(
            email='user1@example.com',
            defaults={
                'phone': '88005535555',
                'city': 'Иваново',
            }
        )
        if created:
            user1.set_password('password123')
            user1.save()

        user1.groups.add(student_group)

        user2, created = User.objects.get_or_create(
            email='user2@example.com',
            defaults={
                'phone': '12345678910',
                'city': 'Москва',
            }
        )
        if created:
            user2.set_password('password123')
            user2.save()

        # Создаем тестовые курсы
        course1, created = Rate.objects.get_or_create(
            name='Python для начинающих',
            defaults={
                'description': 'Базовый курс по Python',
            }
        )

        course2, created = Rate.objects.get_or_create(
            name='Django PRO',
            defaults={
                'description': 'Продвинутый курс по Django',
            }
        )

        # Создаем тестовые уроки
        lesson1, created = Lesson.objects.get_or_create(
            title='Введение в Python',
            defaults={
                'description': 'Основы синтаксиса Python',
                'course': course1,
            }
        )

        # Данные для платежей
        payments_data = [
            {
                'user': user1,
                'payment_date': timezone.make_aware(timezone.datetime(2023, 10, 15, 10, 0)),
                'paid_course': course1,
                'paid_lesson': None,
                'amount': 10000.00,
                'payment_method': 'transfer'
            },
            {
                'user': user2,
                'payment_date': timezone.make_aware(timezone.datetime(2023, 10, 16, 11, 30)),
                'paid_course': None,
                'paid_lesson': lesson1,
                'amount': 2000.00,
                'payment_method': 'cash'
            },
            {
                'user': user1,
                'payment_date': timezone.make_aware(timezone.datetime(2023, 10, 17, 14, 15)),
                'paid_course': course2,
                'paid_lesson': None,
                'amount': 15000.00,
                'payment_method': 'transfer'
            }
        ]

        # Создаем платежи
        for payment_data in payments_data:
            Payments.objects.get_or_create(
                user=payment_data['user'],
                payment_date=payment_data['payment_date'],
                defaults=payment_data
            )

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))