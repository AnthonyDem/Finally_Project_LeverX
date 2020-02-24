from django.contrib.auth.models import User
from rest_framework import serializers
from online_platform.models import Lecture, Task, CompletedTask, Comment, Course, Mark


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

