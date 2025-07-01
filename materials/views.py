from django.shortcuts import render
from rest_framework import viewsets, generics
from materials.serliazers import RateSerializer, LessonSerializer
from materials.models import Rate, Lesson
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrModerator, IsOwner

class RateViewSet (viewsets.ModelViewSet):
    serializer_class = RateSerializer
    queryset = Rate.objects.all()

    def perform_create(self, serializer):
        rate = serializer.save()
        rate.owner = self.request.user
        rate.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsOwnerOrModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        return super().get_permissions()

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    queryset = Lesson.objects.all()

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    queryset = Lesson.objects.all()

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]
    queryset = Lesson.objects.all()

class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Lesson.objects.all()

