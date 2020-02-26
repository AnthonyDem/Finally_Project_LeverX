from django.contrib.auth.base_user import BaseUserManager


class UsersManager(BaseUserManager):
    def create_student(self, email, password, **extra_fields):
        extra_fields.setdefault('is_student', True)
        extra_fields.setdefault('is_active', True)
        if not email:
            raise ValueError('set email please')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_teacher(self, email, password, **extra_fields):
        extra_fields.setdefault('is_teacher', True)
        extra_fields.setdefault('is_active', True)
        if not email:
            raise ValueError('set email please')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        if not email:
            raise ValueError('set email please')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

