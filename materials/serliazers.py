from rest_framework import serializers

from materials.models import Lesson, Rate
from materials.validators import YoutubeFiltrValidator


class RateSerializer(serializers.ModelSerializer):
    lesson_namber = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Rate
        fields = "__all__"

    def get_lesson_namber(self, instance):
        if instance.lesson_set.all():
            return len(instance.lesson_set.all())
        return 0

    def get_lesson(self, instance):
        if instance.lesson_set.all():
            return len(instance.lesson_set.all())
        return 0

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.subscriptions.filter(user=request.user).exists()
        return False


class LessonSerializer(serializers.ModelSerializer):

    video = serializers.TextField(validators=[YoutubeFiltrValidator()])
    read_only_fields = ["owner"]

    class Meta:
        model = Lesson
        fields = "__all__"
