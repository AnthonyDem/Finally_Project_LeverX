from django.contrib.auth.models import User
from rest_framework import serializers
from online_platform.models import Lecture, Task, CompletedTask, Comment, Course, Mark, BaseUser


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'email', 'is_student', 'is_teacher')


class BaseUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('email', 'is_student', 'is_teacher')


class UserRegSerializer(serializers.ModelSerializer):
    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)

    class Meta:
        model = BaseUser
        fields = ('email', 'username', 'password', 'is_student', 'is_teacher')

    def save(self):
        user = BaseUser(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        student = self.validated_data['is_student']
        teacher = self.validated_data['is_teacher']
        if student:
            user.objects.create_student()
            return user
        elif teacher:
            user.objects.create_teacher()
            return teacher


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ('slug',)


class LectureDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('author', 'content', 'course', 'created', 'updated')


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'lecture', 'created', 'updated')


class CompletedTaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedTask
        fields = ('content', 'student', 'task', 'status', 'created', 'updated')


class MarkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('value', 'homework', 'created', 'updated')


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('task', 'name', 'comment', 'created', 'updated')
