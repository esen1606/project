from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password, username=None, **kwargs):
        if not email:
            raise ValueError("В поле электронная почта должна быть указана")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self.create_user(email, password, username, **kwargs)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, validators=[RegexValidator(
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        message='Invalid email address'
    )])
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    role = models.CharField(max_length=10, choices=[('subscriber', 'Подписчик'), ('author', 'Автор')])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = UserManager()
