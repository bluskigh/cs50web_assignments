from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, Listing, Bid, Categories, Comment

class ListingForm(forms.Form):
    title = forms.CharField(max_length=64, label="Title")
    description = forms.CharField(widget=forms.Textarea, max_length=120, 
            label="Description")
    starting_bid = forms.FloatField(localize=False, validators=[
        MinValueValidator(0.9)], label="Staring Bid")
    image = forms.CharField(label="Image Link", max_length=240, required=False)
    options = tuple([(category.id, category.title) for category in Categories.objects.all()])
    categories = forms.MultipleChoiceField(choices=options)


def index(request):
    category = request.GET.get("category")
    listings = Listing.objects.filter(closed=False).all()

    """
    CODE WRITTEN TO DELETE COMMENTS, BUT HAD SOMETHING I LEARNED
    for listing in listings:
        comments = listing.comments.all()
        while len(comments):
            # using listing.comments.remove() does not work for foreignkeys that do not have null=True, 
            # becuase an object can not be deleted from a relation if it never had one in the first place
            listing.comments.filter(id=comments[0].id).delete()
    """

    # filtering by category
    if category is not None:
        listings = [listing for listing in listings if listing.categories.filter(id=category).exists()]

    wll = None
    if request.user.is_authenticated:
        wll = len(request.user.watch_list.all())
    return render(request, "auctions/index.html", 
            {'listings': listings,
                'watch_list_length': wll})


def listings(request):
    return render(request, "auctions/listings.html", {"listings": request.user.listings.all()})


@login_required
def watching(request):
    return render(request, 'auctions/view_watch_list.html', {'listings': 
        request.user.watch_list.all(), 'watch_list_length': 
        len(request.user.watch_list.all())})


@login_required
def add_watching(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        listing.watching.add(request.user)
        return HttpResponseRedirect(reverse("view_listing", kwargs={"listing_id": listing_id}))


@login_required
def remove_watching(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        listing.watching.remove(request.user)
        return HttpResponseRedirect(reverse("view_listing", kwargs={"listing_id": listing_id}))


@login_required(login_url='login')
def view_listing(request, listing_id):
    # TODO show error saying listing was not found if None
    listing = Listing.objects.get(id=listing_id)
    if listing is not None:
        bids = listing.bids.all()
        highest_bid = bids[0] 
        for bid in bids:
            if bid.amount > highest_bid.amount:
                highest_bid = bid
        # below subtracting one from bids_length because 1 is from the owner of the listing 
        return render(request, 'auctions/view_listing.html', 
                {'listing': listing, 'bids_length': len(listing.bids.all())-1, 
                    'highest_bid': highest_bid, 
                    'watch_list_length': len(request.user.watch_list.all()),
                    'watching': listing in request.user.watch_list.all(),
                    'categories': listing.categories.all(), 
                    'comments': listing.comments.all()})
    # return to home page showing error.
    return HttpRedirectResponse(reverse('index'))


def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.closed = True 
    listing.save()
    return HttpResponseRedirect(reverse("view_listing", kwargs=
        {"listing_id": listing_id}))


@login_required
def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        print(request.POST.get('categories'))
        if form.is_valid():
            # add a new listing
            t = form.cleaned_data.get("title")
            d = form.cleaned_data.get("description")
            a = form.cleaned_data.get("starting_bid")
            i = form.cleaned_data.get("image")
            c = form.cleaned_data.get("categories")
            temp_bid = Bid.objects.create(user=request.user, amount=a)
            listing = Listing.objects.create(title=t, description=d, image=i, 
                    owner=request.user)
            # adding the starting bid to the bids
            listing.bids.add(temp_bid)
            # add category to the current listing categories
            for category_id in c:
                category = Categories.objects.get(id=category_id)
                listing.categories.add(category)
            return HttpResponseRedirect(reverse("index"))
    return render(request, 'auctions/add_listing.html', {
        'form': ListingForm(), 'watch_list_length': 
        len(request.user.watch_list.all()), 'categories': Categories.objects.all()})


@login_required
def post_bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if listing is None:
        # show error
        return HttpResponseRedirect(reverse("index"))
    amount = request.POST.get("amount")
    # assuming the field constraints are all correct, and the bid is larger than
    # the largest we will add to bids
    temp_bid_object = Bid.objects.create(user=request.user, amount=amount)
    # add bid to the listings bids association table.
    listing.bids.add(temp_bid_object)
    return HttpResponseRedirect(reverse("view_listing", kwargs={
        "listing_id": listing_id}))


@login_required
def view_categories(request):
    return render(request, 'auctions/view_categories.html', {'categories': 
        Categories.objects.all()})


@login_required
def user_view(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, "auctions/view_user.html", {'found': user is not None, 
        'username': user.username, 'listings': user.listings.all(),
        'watch_list_length': len(request.user.watch_list.all())})


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
