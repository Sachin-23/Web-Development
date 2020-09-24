from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

from django import forms

class Create_listing(forms.Form):
    name = forms.CharField(
            label="Item Name",
            max_length=64,
            widget=forms.TextInput(attrs={"class": "form-control"})
            )
    description = forms.CharField(
            label="Item Description",
            max_length=256,
            widget=forms.Textarea(attrs={"class": "form-control", "rows": "3"})
            )
    intial_bid = forms.IntegerField(
            label="Initial Bid",
            widget=forms.TextInput(attrs={"class": "form-control", "type": "number", "min": "0"})
            )
    url = forms.URLField(
            label="Item URL",
            required=False,
            widget=forms.TextInput(attrs={"class": "form-control"})
            )
    category = forms.CharField(
            label="Category",
            required=False,
            widget=forms.TextInput(attrs={"class": "form-control"})
            )



def index(request):
    all_listing = [i for i in Auction_listing.objects.all() if i.active_listing]
    watchlist = 0
    if request.user.username: 
        current_user = User.objects.get(username=request.user.username)
        watchlist = len(Watchlist.objects.filter(user=current_user))

    return render(request, "auctions/index.html", {
        "title": "Active ",
        "items": all_listing,
        "total_watchlist": watchlist
    })


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



@login_required(login_url="/login")
def create_listing(request):
    all_listing = [i.name for i in Auction_listing.objects.all()]
    form = None
    msg = ""
    if request.method == "POST":
        form = Create_listing(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if name not in all_listing:
                description = form.cleaned_data["description"]
                bid = form.cleaned_data["intial_bid"]
                user = User.objects.get(username=request.user.username)
                if ((url := form.cleaned_data["url"]) == ""):
                    url = "https://indianacademyofdrones.com/wp-content/themes/eikra/assets/img/noimage-420x273.jpg"
                if ((category := form.cleaned_data["category"]) == ""):
                    category = "other"
                new_listing = Auction_listing(name=name, description=description, \
                        initial_bid=bid, user=user, listing_url=url)
                new_listing.save()
                new_cat = Category(category=category, item=new_listing)
                new_cat.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                msg = f"listing with {name} already exist"
    return render(request, "auctions/create_listing.html", {
        "form": form or Create_listing(),
        "msg": msg
        })


@login_required(login_url="/login")
def get_listing(request, name):
    msg = ""
    current_user = User.objects.get(username=request.user.username)
    current_listing = Auction_listing.objects.get(name=name)
    check_watchlist = Watchlist.objects.filter(user=current_user, item=current_listing)
    comments = Comments.objects.filter(comment_item=current_listing)
    bid_users = [(str(i.bid_user), (i.bid_value)) for i in Bids.objects.filter(bid_item=current_listing)]
    bid_users = sorted(bid_users, key= lambda x: x[1])
    if len(bid_users) != 0:
        highest_bid = max(bid_users[-1][1], current_listing.initial_bid)
        highest_bidder = bid_users[-1]
    else:
        highest_bid = current_listing.initial_bid
        highest_bidder = ""
    if request.method == "POST":
        try:
            if "add_watchlist" in request.POST:
                new_watchlist = Watchlist(user=current_user, item=current_listing)
                new_watchlist.save()
            elif "rm_watchlist" in request.POST:
                check_watchlist.delete() 
            elif "add_comment" in request.POST:
                comment = request.POST["comment"]
                if comment != "":
                    new_comment = Comments(comment_user=current_user, \
                            comment_item=current_listing, comment=comment)
                    new_comment.save()
                else: 
                    msg = "Please enter a valid Comment"
            elif "add_bid" in request.POST:
                bid = int(request.POST["bid"])
                if current_user.username in [i[1] for i in bid_users]:
                    new_bid = Bids.objects.get(bid_user=current_user, bid_item=current_listing)
                    new_bid.bid_value = bid
                else:
                    new_bid = Bids(bid_user=current_user, \
                            bid_item=current_listing, bid_value=bid)
                new_bid.save()
            elif "close_bid" in request.POST:
                if len(bid_users) != 0:
                    new_winner = Winners(winner_user=current_user, item=current_listing)
                    current_listing.active_listing = False
                    new_winner.save()
                    current_listing.save()
                else: 
                    msg = "No one has bid yet"
        except Exception as e:
            msg = "Some error occurred, please try again"
        if msg == "":
            return HttpResponseRedirect(reverse("listing", args=[name]))
    return render(request, "auctions/listing.html", {
        "msg": msg,
        "listing": current_listing,
        "check_watchlist": len(check_watchlist),
        "comments": comments,
        "highest_bid": highest_bid,
        "highest_bidder": highest_bidder
        })


@login_required(login_url="/login")
def show_closed_listing(request):
    closed_listing = [i for i in Auction_listing.objects.all() if i.active_listing != True]
    return render(request, "auctions/index.html",  {
        "title": "Closed ",
        "items": closed_listing 
        })
     
@login_required(login_url="/login")
def get_watchlist(request):
    current_user = User.objects.get(username=request.user.username)
    watchlist = Watchlist.objects.filter(user=current_user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        })


@login_required(login_url="/login")
def get_category(request, category=None):
    if category != None:
        items = [i.item for i in Category.objects.filter(category=category) if i.item.active_listing == True]
        return render(request, "auctions/index.html",  {
                "title": category + " ",
                "items": items
            })
    all_category = sorted(set([i.category for i in Category.objects.all()]))
    return render(request, "auctions/category_listing.html", {
        "category": all_category
        })
