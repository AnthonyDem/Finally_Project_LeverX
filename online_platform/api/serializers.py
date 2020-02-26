from django.contrib.auth.models import User
from rest_framework import serializers
from online_platform.models import Lecture, Task, CompletedTask, Comment, Course, Mark, BaseUser


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'name')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'owner', 'teacher', 'students', 'created', 'updated')


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('author', 'content', 'course', 'created', 'updated')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'lecture', 'created', 'updated')


class CompletedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedTask
        fields = ('content', 'student', 'task', 'status', 'created', 'updated')


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('value', 'homework', 'created', 'updated')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('task', 'name', 'comment', 'created', 'updated')
