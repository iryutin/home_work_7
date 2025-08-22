from user.models import CustomUser
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Lesson, Rate


class CourseCRUDTestCase(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = CustomUser.objects.create_user(
            "yv", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        # Создаем тестовый курс
        self.course = Rate.objects.create(
            name="Тестовый курс",
            description="Описание тестового курса",
            owner=self.user,
        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            name="Тестовый урок",
            description="Описание тестового урока",
            video="https://www.youtube.com/watch?v=test",
            rate=self.course,
            owner=self.user,
        )

    def test_create_course(self):
        """Тест создания курса"""
        user = CustomUser.objects.create_user(
            "yv2", email="test2@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=user)
        url = "/api/courses/"
        data = {"name": "Новый курс", "description": "Описание нового курса", "owner": user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rate.objects.count(), 2)
        self.assertEqual(response.data["name"], "Новый курс")

    def test_list_courses(self):
        """Тест получения списка курсов"""
        url = "/api/courses/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_retrieve_course(self):
        """Тест получения конкретного курса"""
        url = f"/api/courses/{self.course.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Тестовый курс")

    def test_delete_course(self):
        """Тест удаления курса"""
        url = f"/api/courses/{self.course.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Rate.objects.count(), 0)

    def test_create_lesson(self):
        """Тест создания урока"""
        url = "/api/lesson/create/"
        data = {
            "name": "Новый урок",
            "description": "Описание нового урока",
            "video": "https://www.youtube.com/watch?v=new",
            "rate": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_list_lessons(self):
        """Тест получения списка уроков"""
        url = "/api/lesson/list/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_lesson(self):
        """Тест получения конкретного урока"""
        url = f"/api/lesson/{self.lesson.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Тестовый урок")

    def test_update_lesson(self):
        """Тест обновления урока"""
        url = f"/api/lesson/update/{self.lesson.id}/"
        data = {
            "name": "Обновленный урок",
            "description": "Обновленное описание урока",
            "video": "https://www.youtube.com/watch?v=updated",
            "rate": self.course.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Обновленный урок")

    def test_delete_lesson(self):
        """Тест удаления урока"""
        url = f"/api/lesson/delite/{self.lesson.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_unauthorized_access(self):
        """Тест доступа без авторизации"""
        self.client.force_authenticate(user=None)
        url = "/api/courses/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_foreign_user_access(self):
        """Тест доступа другого пользователя к чужим курсам"""
        other_user = CustomUser.objects.create_user(
            "yv1", email="test1@example.com", password="otherpass1123"
        )
        self.client.force_authenticate(user=other_user)
        url = f"/api/courses/{self.course.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class VideoURLValidatorTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            "yv", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.course = Rate.objects.create(
            name="Тестовый курс",
            description="Описание тестового курса",
            owner=self.user,
        )

    def test_valid_youtube_url(self):
        """Тест валидной ссылки на YouTube"""
        url = "/api/lesson/create/"
        data = {
            "name": "Урок с YouTube",
            "description": "Описание урока",
            "video": "https://www.youtube.com/watch?v=valid",
            "rate": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

