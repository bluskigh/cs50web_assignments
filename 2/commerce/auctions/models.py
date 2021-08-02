from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    starting_bid = models.FloatField()
    image = models.CharField(max_length=240)
    closed = models.BooleanField(default=False)
