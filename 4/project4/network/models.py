from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Like(models.Model):
    # who the like is by
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name="likes")


class Comment(models.Model):
    # who the comment is by
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
            related_name="comments")
    # the comment
    text = models.CharField(max_length=240)


class Post(models.Model):
    # who the post was created by 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    # title of the post
    title = models.CharField(max_length=64)
    # message of the post
    text = models.CharField(max_length=240)
    # the likes the post has
    likes = models.ManyToManyField(Like, blank=True, related_name="post")
    # when the post was created
    created = models.DateTimeField(auto_now=True)
