from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("view_listing/<int:listing_id>", views.view_listing, name="view_listing"),
    path("users/<int:user_id>", views.user_view, name="user_view"),
    path("post_bid/<int:listing_id>", views.post_bid, name="post_bid")
]
