from django.contrib import admin

from .models import Like, Post, Comment, User, Follow

# Register your models here.
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Follow)
