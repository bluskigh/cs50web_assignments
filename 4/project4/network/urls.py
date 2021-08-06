
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("likes", views.likes, name="likes"),
    path("users/<int:id>", views.users, name="users"),
    path("users/<int:id>/following", views.following, name="following")
]
