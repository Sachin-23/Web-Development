from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

from django import forms

class Create_listing(forms.Form):
    name = forms.CharField(label="", max_length=64, \
            widget=forms.TextInput(attrs={"placeholder": "Name"}))
    description = forms.CharField(label="", max_length=256, \
            widget=forms.TextInput(attrs={"placeholder": "Description"}))
    intial_bid = forms.IntegerField(label="", min_value=0, \
            widget=forms.TextInput(attrs={"placeholder": "Starting Bid"}))
    url = forms.URLField(label="", required=False, \
            widget=forms.TextInput(attrs={"placeholder": "Image url"}))
    category = forms.CharField(label="", required=False, \
            widget=forms.TextInput(attrs={"placeholder": "Catergory"}))


def index(request):
#    print("all listing", all_listing)
    all_listing = [i for i in Auction_listing.objects.all() if i.active_listing]
    watchlist = 0
    if request.user.username: 
        current_user = User.objects.get(username=request.user.username)
        watchlist = len(Watchlist.objects.filter(user=current_user))
    return render(request, "auctions/index.html", {
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
                print(type(form.cleaned_data["url"]))
                if ((url := form.cleaned_data["url"]) == ""):
                    url = "https://indianacademyofdrones.com/wp-content/themes/eikra/assets/img/noimage-420x273.jpg"
                print(type(form.cleaned_data["url"]), url)
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
    msg = ""; winner = ""
    current_listing = Auction_listing.objects.get(name=name) 
    current_user = User.objects.get(username=request.user.username)
    current_bids = Bids.objects.filter(bid_item=current_listing)
    total_comments = Comments.objects.filter(comment_item=current_listing)
    watchlist = Watchlist.objects.filter(user=current_user) 
    total_bids = sorted(current_bids, key=lambda x: x.bid_value, reverse=True)
    if len(total_bids) != 0:
        highest_bid = max([current_listing.initial_bid, total_bids[0].bid_value])
    else:
        highest_bid = current_listing.initial_bid
    total_bidders = [(i.bid_user, i.bid_value) for i in current_bids \
            if str(i.bid_user) == str(request.user.username)]
    if request.method == "POST":
        if "new_bid" in request.POST:
            bid = request.POST["bid"]
            new_bid = Bids(bid_user=current_user, bid_item=current_listing, \
                    bid_value=bid)
            new_bid.save()
        elif "close_bid" in request.POST: 
            current_listing.active_listing = False; #make changes
            current_listing.save()
            win_user = total_bids[-1].bid_user
            winner = Winners(winner_user=win_user, item=current_listing)
            winner.save()
            winner = winner.winner_user
        elif "submit_comment" in request.POST:
           comment = request.POST["comment"]
           new_comment = Comments(comment_user=current_user, \
                   comment_item=current_listing, comment=comment)
           new_comment.save()
        elif "add_watchlist" in request.POST:
            new_watchlist = Watchlist(user=current_user, item=current_listing) 
            new_watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=[name]))
    return render(request, "auctions/listing.html", {
        "item": current_listing,
        "category": Category.objects.get(item=current_listing),
        "highest_bidders": highest_bid,
        "total_bidders": total_bidders,
        "some_list": total_bids,
        "comments": total_comments,
        "watchlist": watchlist
        })


@login_required(login_url="/login")
def show_closed_listing(request):
    closed_listing = [i for i in Auction_listing.objects.all() if i.active_listing != True]
    return render(request, "auctions/index.html",  {
        "items": closed_listing 
        })
     
@login_required(login_url="/login")
def get_watchlist(request):
    current_user = User.objects.get(username=request.user.username)
    watchlist = Watchlist.objects.filter(user=current_user)
    print(len(watchlist))
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        })


@login_required(login_url="/login")
def get_category(request, category=None):
    if category != None:
        items = [i.item for i in Category.objects.filter(category=category)]
        return render(request, "auctions/index.html",  {
                "items": items
            })
    all_category = set([i.category for i in Category.objects.all()])
    return render(request, "auctions/category_listing.html", {
        "category": all_category
        })
    



