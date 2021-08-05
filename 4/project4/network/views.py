from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from json import loads

from .models import User, Comment, Like, Post


class PostForm(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs=
        {"placeholder": "Enter title"}))
    text = forms.CharField(max_length=240, widget=forms.Textarea(attrs=
        {"placeholder": "Enter your message..."}))


def index(request):
    return render(request, "network/index.html", {"new_post_form": PostForm(),
        "posts": Post.objects.all(), "edit_post_form": PostForm()})


@login_required
def posts(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            print(type(cd))
            Post.objects.create(title=cd.get("title"), text=cd.get("text"),
                user=request.user)
        return HttpResponseRedirect(reverse("index"))
    # TODO change this 
    return Http404('You are not supposed to get here.')


@login_required
def edit_post(request, id):
    post = Post.objects.get(id=id)
    if post is None:
        return Http404(f"Could not find post of id: {id}")
    if post.user.id != request.user.id:
        return HttpResponse("Unauthorized", status=401) 
    if request.method == "GET":
        return JsonResponse({"title": post.title, "text": post.text})
    elif request.method == "PATCH":
        try:
            # getting data sent via json
            data = loads(request.body)
            title = data.get("title")
            text = data.get("text")
            if title is not None and (title != post.title):
                post.title = title
            if text is not None and (text != post.text):
                post.text = text
            post.save()
            return HttpResponse("Updated", status=204)
        except Exception as e:
            print(e)
            return HttpResponse("Server Error", status=500)


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
