from django.db import models

from django.contrib.auth.models import User
from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_post_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.PROTECT, related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.PROTECT, related_name='topics')
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')
    update_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='+')

    def __str__(self):
        truncated_message= Truncator(self.message)
        return truncated_message.chars(30)





