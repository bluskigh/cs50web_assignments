from datetime import datetime
from json import loads

from django import forms
from django.contrib.auth import (
        authenticate, 
        login, 
        logout 
)
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import (
        HttpResponse, 
        HttpResponseRedirect, 
        Http404, 
        JsonResponse
)
from django.shortcuts import render
from django.urls import reverse

from .models import User, Comment, Post, Follow


class PostForm(forms.Form):
    # title = forms.CharField(max_length=64, widget=forms.TextInput(attrs=
        # {"placeholder": "Enter title"}))
    text = forms.CharField(max_length=240, widget=forms.Textarea(attrs=
        {"placeholder": "Enter your message..."}))


def get_posts(request, posts):
    """ Returns 10 post depending on the start and end that is found in the
    url arguments."""
    posts = [post.clean() for post in posts]
    page = int(request.GET.get("page") or 0)
    start = page * 10
    end = start + 10
    return posts[start:end]


def get_limited(posts, limit):
    viewed = {}
    final = []
    for post in posts:
        if viewed.get(post.user.id) is None:
            viewed[post.user.id] = 1
        if viewed[post.user.id] <= limit:
            final.append(post)
            viewed[post.user.id] += 1
    return final 


def index(request):
    return render(request, "network/index.html", {
        "new_post_form": PostForm(),
        "edit_post_form": PostForm()})


@login_required
def users(request, id):
    user = User.objects.get(id=id)
    if user is None:
        return Http404(f"Could not find user with id of: {id}")
    return render(request, "network/view_user.html", {
        "id": user.id,
        "username": user.username,
        "followers": user.followers.count(),
        "following": user.following.count(),
        "is_following": request.user.following.filter(
            to__id=user.id).exists() if request.user.id != id else None,
        "edit_post_form": PostForm()})


def posts(request):
    # Could have filtered by id since the highest id is the most recent post. 
    # added by the user, but wanted to work with time. 
    if request.method == "GET":
        userid = request.GET.get("userid")
        following = request.GET.get("following")
        page = int(request.GET.get("page") or 1) + 1
        posts = None
        if request.GET.get("following"):
            # following page requirement: show less posts from users 
            if request.user.following.count() == 0:
                return JsonResponse({
                    "reason": "You're not following anyone"}, status=400)
            posts = get_limited([post for user in 
                request.user.following.all() 
                for post in user.to.posts.order_by("-created__time")], 3)
        elif userid:
            # viewing user show all posts
            posts = User.objects.get(id=int(userid)).posts.filter(
                    user__id=userid).order_by("-created__time")
        else:
            # on view all posts page, show 5 per user
            posts = get_limited(Post.objects.order_by("-created__time"), 5)
        # returning userid because on js we want to determine if a
        # post is the users posts that is making the request, to add edit
        # button to the relative post.
        return JsonResponse({
            "posts":  get_posts(request, posts), 
            "userid": request.user.id,
            "is_more": len(posts) - page*10 > 0})
    elif request.method == "POST" and request.user.is_authenticated:
        data = loads(request.body) 
        if data.get("text") is None:
            return HttpResponse("Bad Request", status=400)
        post = Post.objects.create(text=data.get("text"), user=request.user)
        return JsonResponse(post.clean()) 
    elif request.method == "PATCH" and request.user.is_authenticated:
        # getting data sent via json
        id = request.GET.get("id")
        if id is None:
            return Http404("Missing id value")
        post = Post.objects.get(id=id)
        if post is None:
            return Http404(f"Could not find post of id: {id}")
        # checking if the user who is making the request is the owner 
        # of the post
        if post.user.id != request.user.id:
            return HttpResponse("Unauthorized", status=401) 
        data = loads(request.body)
        text = data.get("text")
        if text is not None and (text != post.text):
            post.text = text
        post.updated = True
        post.save()
        return HttpResponse("Updated", status=200)


def likes(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=409)
    id = loads(request.body).get("post_id")
    if id is None:
            return HttpResponse("Bad Request", status=300)
    post = Post.objects.get(id=id)
    if post is None:
        return Http404(f"Could not find a post with id of: {id}")
    if request.method == "POST":
        # check if the user already liked
        if post.likes.filter(id=request.user.id).exists():
            return HttpResponse(status=409)
        # add a like that belongs to the user
        post.likes.add(request.user)
        # post.likes.create(user=request.user)
        return HttpResponse(status=200)
    elif request.method == "DELETE":
        # remove from liked
        like = post.likes.get(id=request.user.id)
        post.likes.remove(like)
        return HttpResponse(status=200)


@login_required
def following(request, id=None):
    if request.method == "GET":
        return render(request, "network/view_following.html")
    user = User.objects.get(id=id)
    if user is None:
        return Http404(f"Could not find user id of: {id}")
    message = None 
    if request.method == "POST":
        # check if already following the user
        if request.user.following.filter(to__id=user.id).exists():
            return HttpResponse("Already following this user.", status=409)
        Follow.objects.create(who=request.user, to=user)
        message = "Followed the user"
    elif request.method == "DELETE":
        # unfollow the user
        request.user.following.filter(to__id=user.id).delete()
        message = "Unfollowed the user"
    return HttpResponse(message, status=200)


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
