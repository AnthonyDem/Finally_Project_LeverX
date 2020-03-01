from django.contrib.auth.models import User
from rest_auth.registration.serializers import VerifyEmailSerializer
from rest_framework import serializers, generics
from online_platform.models import Lecture, Task, CompletedTask, Comment, Course, Mark, BaseUser


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'email', 'is_student', 'is_teacher')


class BaseUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('email', 'is_student', 'is_teacher')


class UserRegSerializer(VerifyEmailSerializer):
    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)

    class Meta:
        model = BaseUser
        fields = ('email', 'password', 'is_student', 'is_teacher')


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


'''
class UserRegSerializer(RegisterSerializer):
    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)

    class Meta:
        model = BaseUser
        fields = ('email', 'password', 'is_student', 'is_teacher')


    def save(self, request):
        """stud_role = self.validated_data['is_student']
        teach_role = self.validated_data['is_teacher']
        if stud_role:
            stud = BaseUser.objects.create_student(self.validated_data['email'], self.validated_data['password'])
            DefaultAccountAdapter.confirm_email(request, stud[''])
            stud.save()
            return stud
        elif teach_role:
            teach = BaseUser.objects.create_teacher(self.validated_data['email'], self.validated_data['password'])
            teach.save()
            return teach"""


'''