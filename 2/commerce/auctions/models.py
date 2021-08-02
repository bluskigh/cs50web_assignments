from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    image = models.CharField(max_length=240)
    closed = models.BooleanField(default=False)
    watching = models.ManyToManyField(User, blank=True, related_name="watch_list")
    bids = models.ManyToManyField(Bid, blank=True, related_name="listing")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, 
            related_name="listings")
