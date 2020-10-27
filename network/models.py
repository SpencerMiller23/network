from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    text = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    likes = models.ManyToManyField(User, blank=True, related_name="liked_by")
    timestamp = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, blank=True, related_name="is_follower")
    following = models.ManyToManyField(User, blank=True, related_name="is_following")
