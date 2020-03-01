from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from rest_auth.registration.serializers import VerifyEmailSerializer
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from online_platform.models import Lecture, Course, Task, CompletedTask, Comment, BaseUser
from .serializers import (LectureDetailSerializer, TaskDetailSerializer,
                          CompletedTaskDetailSerializer, CommentDetailSerializer,
                          BaseUserSerializer, CourseDetailSerializer)
from online_platform.permissions import (IsOwnerOrReadOnly, IsNotYourClassroom,
                                         IsStudentOrReadOnly, IsTeacherOrReadOnly)
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view()
def django_rest_auth_null():
    return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        try:
            confirmation = self.get_object()
            confirmation.confirm(self.request)
            return Response({'detail': _('Successfully confirmed email.')}, status=status.HTTP_200_OK)
        except EmailConfirmation.DoesNotExist:
            return Response({'detail': _('Error. Incorrect key.')}, status=status.HTTP_404_NOT_FOUND)

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        emailconfirmation = EmailConfirmationHMAC.from_key(key)
        if not emailconfirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                emailconfirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                raise EmailConfirmation.DoesNotExist
        return emailconfirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs


class UserListView(generics.ListAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = Course.objects.filter(students=user)
        elif user.is_teacher:
            queryset = Course.objects.filter(teachers=user)
        elif user.is_superuser:
            queryset = Course.objects.all()
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(teachers=(user,))


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()
    permission_classes = (IsAuthenticated, IsTeacherOrReadOnly,
                          IsNotYourClassroom)


class LectureListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = Lecture.objects.filter(
                course__students=user
            )
        elif user.is_teacher:
            queryset = Lecture.objects.filter(
                course__teachers=user
            )
        elif self.request.user.is_superuser:
            queryset = Lecture.objects.all()
        return queryset


class LectureDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LectureDetailSerializer
    permission_classes = (IsAuthenticated,
                          IsTeacherOrReadOnly)
    queryset = Lecture.objects.all()


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureDetailSerializer
    permission_classes = (IsAuthenticated,
                          IsTeacherOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = Task.objects.filter(
                lectures__course__students=user
            )
        elif user.is_teacher:
            queryset = Task.objects.filter(
                lectures__course__teachers=user  # lecture
            )
        elif user.is_superuser:
            queryset = Task.objects.all()

        return queryset


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,
                          IsTeacherOrReadOnly)


class CompletedtaskListCreateView(generics.ListCreateAPIView):
    serializer_class = CompletedTaskDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = CompletedTask.objects.filter(
                student=user
            )
        elif user.is_teacher:
            queryset = CompletedTask.objects.filter(
                task__lectures__course_teachers=user  # lecture
            )
        elif user.is_superuser:
            queryset = CompletedTask.objects.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class CompletedtaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompletedTaskDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            self.permission_classes = (IsStudentOrReadOnly,)
        elif user.is_teacher:
            self.permission_classes = (IsTeacherOrReadOnly,)
        return CompletedTask.objects.all


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Comment.objects.filter(task=self.kwargs['pk'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseLecturesListView(generics.ListCreateAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrReadOnly)

    def get_queryset(self):
        queryset = Lecture.objects.filter(course=self.kwargs['pk'])
        return queryset


class LectureTasksListView(generics.ListCreateAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrReadOnly)

    def get_queryset(self):
        queryset = Task.objects.filter(lectures=self.kwargs['pk'])
        return queryset
