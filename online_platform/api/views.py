from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from online_platform.models import Lecture, Course, Task, CompletedTask, Comment, BaseUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from .permissions import (IsOwnerOrReadOnly, IsNotYourClassroom,
                          IsStudentOrReadOnly, IsTeacherOrReadOnly, IsStudent, IsTeacherOrStudentWorker)
from .serializers import (LectureDetailSerializer, TaskDetailSerializer,
                          CompletedTaskDetailSerializer, CommentDetailSerializer,
                          BaseUserSerializer, CourseDetailSerializer, UserRegSerializer,
                          MarkDetailSerializer)


@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserRegSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered a new user'
            data['email'] = user.email
            data['username'] = user.username
            data['is_student'] = user.is_student
            data['is_teacher'] = user.is_teacher
            token = Token.objects.get(user=user)
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


@permission_classes([IsAdminUser, ])
class UserListView(generics.ListAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer


@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseDetailSerializer

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


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly, IsNotYourClassroom])
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class LectureListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = Lecture.objects.filter(
                courses__students=user
            )
        elif user.is_teacher:
            queryset = Lecture.objects.filter(
                courses__teachers=user
            )
        elif self.request.user.is_superuser:
            queryset = Lecture.objects.all()
        return queryset


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class LectureDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LectureDetailSerializer
    queryset = Lecture.objects.all()


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = Task.objects.filter(
                lectures__courses__students=user
            )
        elif user.is_teacher:
            queryset = Task.objects.filter(
                lectures__courses__teachers=user  # lecture
            )
        elif user.is_superuser:
            queryset = Task.objects.all()

        return queryset


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()


@permission_classes([IsAuthenticated, IsStudentOrReadOnly])
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
                task__lectures__courses__teachers=user  # lecture
            )
        elif user.is_superuser:
            queryset = CompletedTask.objects.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


@permission_classes([IsAuthenticated, ])
class CompletedtaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompletedTaskDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            self.permission_classes = (IsStudentOrReadOnly,)
        elif user.is_teacher:
            self.permission_classes = (IsTeacherOrReadOnly,)
        return CompletedTask.objects.all()


@permission_classes([IsAuthenticated, IsTeacherOrStudentWorker])
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentDetailSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(comments=self.kwargs['pk'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class CourseLecturesListView(generics.ListCreateAPIView):
    serializer_class = CourseDetailSerializer

    def get_queryset(self):
        queryset = Lecture.objects.filter(courses=self.kwargs['pk'])
        return queryset


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class LectureTasksListView(generics.ListCreateAPIView):
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(lectures=self.kwargs['pk'])
        return queryset


@permission_classes([IsAuthenticated, IsStudent])
class MarkListView(generics.ListAPIView):
    serializer_class = MarkDetailSerializer

    def get_queryset(self):
        queryset = CompletedTask.objects.filter(student=self.request.user)
        return queryset
