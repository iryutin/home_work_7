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
router.register(r"rate", RateViewSet, basename="rate")
urlpatterns = [
    path("create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("view/", LessonListAPIView.as_view(), name="lesson_view"),
    path("view/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_get"),
    path("view/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("view/delite/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delite"),
] + router.urls
