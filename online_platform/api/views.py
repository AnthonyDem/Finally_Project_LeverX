from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from online_platform.models import Lecture, Course, Task, CompletedTask, Mark, Comment, BaseUser
from .serializers import (LectureSerializer, CourseSerializer, TaskSerializer,
                          CompletedTaskSerializer, MarkSerializer, CommentSerializer, BaseUserSerializer)

class CourseView(ListModelMixin):
    pass
