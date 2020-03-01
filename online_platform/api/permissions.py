from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_teacher


class IsStudentOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_student


class IsNotYourClassroom(permissions.BasePermission):
    message = 'Your haven\'t access to this classroom'

    def has_object_permission(self, request, view, obj):
        if request.user.is_teacher:
            return request.user in obj.teachers.all()
        elif request.user.is_student:
            return request.user in obj.students.all()



