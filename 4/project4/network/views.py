from datetime import datetime
from json import loads

from django import forms
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Comment, Like, Post, Follow


class PostForm(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs=
        {"placeholder": "Enter title"}))
    text = forms.CharField(max_length=240, widget=forms.Textarea(attrs=
        {"placeholder": "Enter your message..."}))


def get_posts(request, posts):
    """ Returns 10 post depending on the start and end that is found in the
    url arguments"""
    page = int(request.GET.get("page") or 1) - 1
    start = page * 10
    end = start + 10
    posts = reverse_chronological_order(posts)
    return posts[start:end]


def is_more_to_load(request):
    # the end of the current user, ex currently viewing 0 - 10, in order
    # for next to show we want to know if there is more than the current
    # end... 10, are there 11 posts? if so show next button (return true)
    page = request.GET.get("page") or 1 
    return JsonResponse({"result": Post.objects.count() - int(page)*10 > 0})


def reverse_chronological_order(posts):
    # from chronological order to reverse chronological order
    posts = [post.clean() for post in posts]
    for index, post in enumerate(posts):
        if index == len(posts)//2:
            break
        temp = posts[index]
        posts[index] = posts[-index-1]
        posts[-index-1] = temp
    return posts


def index(request):
    return render(request, "network/index.html", {
        "new_post_form": PostForm(),
        "edit_post_form": PostForm()})


@login_required
def users(request, id):
    user = User.objects.get(id=id)
    if user is None:
        return Http404(f"Could not find user with id of: {id}")
    is_following = None
    if request.user.id != id:
        is_following = request.user.following.filter(to__id=user.id).exists()
    return render(request, "network/view_user.html", {
        "id": user.id,
        "username": user.username,
        "followers": user.followers.all(),
        "following": user.following.all(),
        "is_following": is_following
        })


@login_required
def posts(request):
    if request.method == "GET":
        # if attempting to get a specific post 
        if request.GET.get("id"):
            post = Post.objects.get(id=request.GET.get("id"))
            return JsonResponse({"title": post.title, "text": post.text})
        # otherwise return all posts
        else:
            return JsonResponse({"posts":  get_posts(request, 
                Post.objects.all())})
    elif request.method == "POST":
        data = loads(request.body) 
        if data.get("title") is None or data.get("text") is None:
            return HttpResponse("Bad Request", status=400)
        post = Post.objects.create(title=data.get("title"), 
                text=data.get("text"),
            user=request.user)
        print(post.created)
        return JsonResponse(post.clean()) 
    elif request.method == "PATCH":
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
        try:
            data = loads(request.body)
            title = data.get("title")
            text = data.get("text")
            if title is not None and (title != post.title):
                post.title = title
            if text is not None and (text != post.text):
                post.text = text
            post.save()
            return HttpResponse("Updated", status=200)
        except Exception as e:
            print(e)
            return HttpResponse("Server Error", status=500)
    # TODO change this 
    return Http404('You are not supposed to get here.')


def likes(request):
    id = loads(request.body).get("post_id")
    if id is None:
            return HttpResponse("Bad Request", 300)
    post = Post.objects.get(id=id)
    if post is None:
        return Http404(f"Could not find a post with id of: {id}")
    if request.method == "POST":
        # check if the user already liked
        # using field clause = WHERE clause in SQL -> https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups
        if post.likes.filter(user__id=request.user.id).exists():
            return HttpResponse(status=409)
        # add a like that belongs to the user
        post.likes.create(user=request.user)
        return HttpResponse(status=200)
    elif request.method == "DELETE":
        # remove from liked
        like = post.likes.get(user__id=request.user.id)
        # remove from database, which will remove from post likes too?
        like.delete()
        return HttpResponse(status=200)


@login_required
def following(request, id=None):
    if request.method == "GET":
        posts = []
        for following in request.user.following.all():
            # for relevancy reasons, showing the top 3 most recent posts
            for post in reverse_chronological_order(list(
                following.to.posts.all())[-4:-1]):
                posts.append(post)
        return render(request, "network/view_following.html", {
            "posts": posts
            })
    # otherwise might be a delete or post request
    user = User.objects.get(id=id)
    if user is None:
        return Http404(f"Could not find user id of: {id}")
    message = None 
    # if not data.get("following_state"): 
    if request.method == "POST":
        # follow the user
        # check if already following the user
        if request.user.following.filter(to__id=user.id).exists():
            return HttpResponse(409)
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
