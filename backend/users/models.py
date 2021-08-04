from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model."""
    email = models.EmailField(max_length=100,
                              verbose_name="email",
                              null=False, unique=True)
    username = models.CharField(max_length=150,
                                verbose_name="username",
                                unique=True)
    first_name = models.CharField(max_length=150,
                                  verbose_name="first_name")
    last_name = models.CharField(max_length=150,
                                 verbose_name="last_name")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
