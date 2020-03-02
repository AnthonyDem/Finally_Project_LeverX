from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .api.views import (CourseDetailView, CourseListCreateView, UserListView, CourseLecturesListView,
                        LectureDetailView, LectureListCreateView, LectureTasksListView, TaskListCreateView,
                        TaskDetailView, CompletedtaskDetailView, CompletedtaskListCreateView, CommentListView,
                        registration_view, MarkListView)

app_name = 'online_platform'

urlpatterns = [
    path('/auth/', include('rest_framework.urls')),
    path('/register/', registration_view, name='register'),
    path('/login/', obtain_auth_token, name='login'),
    path('/users/', UserListView.as_view()),
    path('/courses/', CourseListCreateView.as_view()),
    path('/courses/<int:pk>/', CourseDetailView.as_view()),
    path('/courses/<int:pk>/lectures', CourseLecturesListView.as_view()),
    path('/lectures/', LectureListCreateView.as_view()),
    path('/lectures/<int:pk>/', LectureDetailView.as_view()),
    path('/lectures/<int:pk>/tasks/', LectureTasksListView.as_view()),
    path('/marks/', MarkListView.as_view()),
    path('/tasks/', TaskListCreateView.as_view()),
    path('/tasks/<int:pk>', TaskDetailView.as_view()),
    path('/completed/', CompletedtaskListCreateView.as_view()),
    path('/completed/<int:pk>/', CompletedtaskDetailView.as_view()),
    path('/completed/<int:pk>/comments/', CommentListView.as_view())
]

