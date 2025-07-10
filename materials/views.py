from django.shortcuts import render
from rest_framework import viewsets, generics
from materials.serliazers import RateSerializer, LessonSerializer
from materials.models import Rate, Lesson
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrModerator, IsOwner



class RateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing courses (Rate).
    - POST: Create a new course (owner is set to the current user).
    - GET: List or retrieve courses.
    - PUT/PATCH: Update a course (owner or moderator only).
    - DELETE: Delete a course (owner only).
    """
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
    """
    Create a new lesson. Only authenticated users can create lessons. The owner is set to the current user.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """
    List all lessons. Only authenticated users who are owners or moderators can view lessons.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Retrieve a specific lesson by ID. Only owners or moderators can retrieve lessons.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Update a lesson by ID. Only owners or moderators can update lessons.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Delete a lesson by ID. Only the owner can delete lessons.
    """
    permission_classes = [IsOwner]
    queryset = Lesson.objects.all()
