from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render 
from django.urls import reverse
from django.core.validators import MinValueValidator
from django import forms

from .models import User, Listing


class ListingForm(forms.Form):
    title = forms.CharField(max_length=64, label="Title")
    description = forms.CharField(widget=forms.Textarea, max_length=120, 
            label="Description")
    starting_bid = forms.FloatField(localize=False, validators=[
        MinValueValidator(0.9)], label="Staring Bid")
    image = forms.CharField(label="Image Link", max_length=240)


def index(request):
    return render(request, "auctions/index.html", 
            {'listings': Listing.objects.filter(closed= False).all()})


def view_listing(request, listing_id):
    # TODO show error saying listing was not found if None
    listing = Listing.objects.get(id=listing_id)
    if listing is not None:
        return render(request, 'auctions/view_listing.html', {'listing': 
                                                                listing})
    # return to home page showing error.
    return HttpRedirectResponse(reverse('index'))


def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            # add a new listing
            t = form.cleaned_data.get("title")
            d = form.cleaned_data.get("description")
            b = form.cleaned_data.get("starting_bid")
            i = form.cleaned_data.get("image")
            Listing.objects.create(title=t, description=d, starting_bid=b, image=i)
            return HttpResponseRedirect(reverse("index"))
    return render(request, 'auctions/add_listing.html', {
        'form': ListingForm()})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
