from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Rate

from .models import Subscription, CustomUser


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        # Создаем тестовый курс
        self.course = Rate.objects.create(
            name="Тестовый курс",
            description="Описание тестового курса",
            owner=self.user,
        )

    def test_create_subscription(self):
        """Тест создания подписки"""
        url = reverse("subscription")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_remove_subscription(self):
        """Тест удаления подписки"""
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse("subscription")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_status_in_course(self):
        """Тест отображения статуса подписки в курсе"""
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse("course-detail", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_subscribed"])

    def test_no_subscription_status_in_course(self):
        """Тест отображения отсутствия подписки в курсе"""
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_subscribed"])

    def test_subscription_unauthorized(self):
        """Тест подписки без авторизации"""
        self.client.force_authenticate(user=None)
        url = reverse("subscription")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
