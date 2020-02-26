from django.contrib import admin
from .models import Lecture, Task, CompletedTask, Comment, Course, Mark, BaseUser
# Register your models here.
admin.site.register(BaseUser)
admin.site.register(Lecture)
admin.site.register(Task)
admin.site.register(CompletedTask)
admin.site.register(Comment)
admin.site.register(Course)
admin.site.register(Mark)