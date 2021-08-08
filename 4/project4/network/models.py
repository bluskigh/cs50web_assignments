from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Follow(models.Model):
    # the person that is following
    who = models.ForeignKey(User, on_delete=models.CASCADE, 
            related_name="following") 
    # the person that is being followed
    to = models.ForeignKey(User, on_delete=models.CASCADE, 
            related_name="followers") 


class Comment(models.Model):
    # who the comment is by
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
            related_name="comments")
    # the comment
    text = models.CharField(max_length=240)


class Post(models.Model):
    # who the post was created by 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    # message of the post
    text = models.CharField(max_length=240)
    # the likes the post has
    likes = models.ManyToManyField(User, blank=True, related_name="post")
    # when the post was created
    created = models.DateTimeField(auto_now=True)
    # determines if the user updated the post since its creation
    updated = models.BooleanField(default=False)

    def clean(self):
        return {"id": self.id, "text": self.text, 
                "likes": [user.id for user in self.likes.all()], 
                "created": self.created.strftime("%y-%m-%d %a %H:%M %p"), 
                "user_id": self.user.id, "username": self.user.username,
                "updated": self.updated}
