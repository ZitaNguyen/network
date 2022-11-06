from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey('User', on_delete=models.CASCADE, related_name='poster')
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    number_of_like = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.poster}"


class FollowList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user')
    followings = models.ManyToManyField('User', related_name='followings', blank=True)
    followers = models.ManyToManyField('User', related_name='followers', blank=True)

    def __str__(self):
        return f"{self.user}"