"""Desctibe User models."""

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    """User model."""

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=88)
    email = models.EmailField(max_length=70, unique=True)
    last_login = models.DateTimeField(auto_now_add=True)
