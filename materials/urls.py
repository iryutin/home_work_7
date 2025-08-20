from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    RateViewSet,
)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", RateViewSet, basename="course")  # исправлено на courses

urlpatterns = [
    path("create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("view/", LessonListAPIView.as_view(), name="lesson-list"),
    path("view/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-detail"),
    path("view/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("view/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"),
] + router.urls
