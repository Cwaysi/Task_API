from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        other_fields.setdefault(role="User")
        other_fields.setdefault('is_active', True)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_admin(self, email, password=None, **other_fields):
        other_fields.setdefault(role="Admin")
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)


class CustomUser(AbstractUser, PermissionsMixin):

    ROLE={
        ("Admin", "Admin"),
        ("User", "User")
    }

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=225)
    role = models.CharField(max_length=6, choices=ROLE, default="User")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = "email"  #making email the username 

    def __str__(self):
        return f"{self.full_name} - {self.email}"
