from django.urls import path, include, re_path
from allauth.account.views import confirm_email
from rest_auth.registration.views import RegisterView, VerifyEmailView
from .api.views import (CourseDetailView, CourseListCreateView, UserListView, CourseLecturesListView,
                        LectureDetailView, LectureListCreateView, LectureTasksListView, TaskListCreateView,
                        TaskDetailView, CompletedtaskDetailView, CompletedtaskListCreateView, CommentListView,
                        django_rest_auth_null)

app_name = 'online_platform'


urlpatterns = [
    path('', include('rest_auth.urls')),
    path('/registration/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('/registration/', include('rest_auth.registration.urls')),
    path('/rest-auth/registration/account-email-verification-sent/', django_rest_auth_null,
         name='account_email_verification_sent'),
    path('/users/', UserListView.as_view()),
    path('/courses/', CourseListCreateView.as_view()),
    path('/courses/<int:pk>/', CourseDetailView.as_view()),
    path('/courses/<int:pk>/lectures', CourseLecturesListView.as_view()),
    path('/lectures/', LectureListCreateView.as_view()),
    path('/lectures/<int:pk>/', LectureDetailView.as_view()),
    path('/lectures/<int:pk>/tasks/', LectureTasksListView.as_view()),
    path('/tasks/', TaskListCreateView.as_view()),
    path('/tasks/<int:pk>', TaskDetailView.as_view()),
    path('/completed/', CompletedtaskListCreateView.as_view()),
    path('/completed/<int:pk>/', CompletedtaskDetailView.as_view()),
    path('/completed/<int:pk>/comments/', CommentListView.as_view())
]

# path('/auth/', include('rest_auth.urls')),
# path('/auth/registration/', include('rest_auth.registration.urls')),
# path('/auth/', include('djoser.urls')),
# path('/auth/', include('djoser.urls.authtoken')),
# path('/auth/', include('djoser.urls.jwt')),