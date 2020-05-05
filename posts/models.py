"""Desctibe Post models."""

from django.db import models

from users.models import User


class Post(models.Model):
    """Post model."""

    title = models.CharField(max_length=30)
    body = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
    """Like model."""

    post_id = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
