from rest_framework import serializers
from materials.models import Rate, Lesson

class RateSerializer(serializers.ModelSerializer):
    lesson_namber = serializers.SerializerMethodField()

    class Meta:
        model = Rate
        fields = '__all__'

    def get_lesson_namber(self, instance):
        if instance.lesson_set.all():
            return len(instance.lesson_set.all())
        return 0

    def get_lesson(self, instance):
        if instance.lesson_set.all():
            return len(instance.lesson_set.all())
        return 0

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'