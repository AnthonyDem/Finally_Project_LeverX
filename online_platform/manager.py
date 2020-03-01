from django.contrib.auth.base_user import BaseUserManager


class UsersManager(BaseUserManager):
    def create_user(self, email, password, is_active=True, **extra_fields):
        if not email:
            raise ValueError('set email please')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = is_active
        user.save()
        return user

    def create_student(self, email, password, **extra_fields):
        extra_fields.setdefault('is_student', True)

        return self.create_user(email, password, **extra_fields)

    def create_teacher(self, email, password, **extra_fields):
        extra_fields.setdefault('is_teacher', True)

        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)