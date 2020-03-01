from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from .manager import UsersManager


# Create your models here.

def content_completed_tasks(instance, filename):
    return '/'.join(['content', 'completed_tasks']) + f'{instance.student}/{filename}'


def content_lectures(instance, filename):
    return '/'.join(['content', 'lectures']) + f'{instance.course}/{filename}'


class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=250 , blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsersManager()

    def __str__(self):
        return self.email


class Course(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=250)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teachers',
                                      limit_choices_to={'is_teacher': True})
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='students', blank=True,
                                      limit_choices_to={'is_student': True})
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Lecture(models.Model):
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.FileField(upload_to=content_lectures)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses')


class Task(models.Model):
    title = models.CharField(max_length=250)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='lectures')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class CompletedTask(models.Model):
    STATUS_CHOICES = (
        ('graded', 'Graded'),
        ('turned_in', 'Turned in'),
        ('no_data', 'No data yet')
    )
    content = models.FileField(upload_to=content_completed_tasks)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                limit_choices_to={'is_student': True})
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default='no_data')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return 'Task: {} Student: {}'.format(self.task, self.student)


class Mark(models.Model):
    value = models.PositiveIntegerField(default=100)
    homework = models.OneToOneField(CompletedTask, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class Comment(models.Model):
    task = models.ForeignKey(Mark, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return "Comment by {} on {}".format(self.name, self.task)
