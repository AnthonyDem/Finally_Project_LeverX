from django.shortcuts import get_object_or_404
from rest_framework import permissions

from online_platform.models import CompletedTask


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_teacher


class IsStudentOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_student


class IsStudent(permissions.BasePermission):
    message = 'You are not a student'

    def has_permission(self, request, view):
        return request.user.is_student

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


class IsNotYourClassroom(permissions.BasePermission):
    message = 'Your haven\'t access to this classroom'

    def has_object_permission(self, request, view, obj):
        if request.user.is_teacher:
            return request.user in obj.teachers.all()
        elif request.user.is_student:
            return request.user in obj.students.all()


class IsTeacherOrStudentWorker(permissions.BasePermission):
    message = 'you haven\'t access'

    def has_permission(self, request, view):
        if request.user.is_teacher:
            return request.user in CompletedTask.task.lectures.courses.teachers.all()
        elif request.user.is_student:
            return request.user == CompletedTask.student
