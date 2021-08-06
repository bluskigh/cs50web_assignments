from django.contrib import admin

from .models import Like, Post, Comment

# Register your models here.
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Comment)
