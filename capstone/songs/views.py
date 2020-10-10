from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from .models import *

def index(request):
    if request.user.is_authenticated:
        return HttpResponse("<h1>&#x1F3B6; Index</h1>")
    else:
        return HttpResponse("<h1>&#x1F3B6;</h1>")

def login_view(request):
    return render(request, "songs/login_register.html")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        return HttpResponse(f"{username} {password}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("center"))
        else:
            return HttpResponse("Login Failed")
            #return render(request,)
    else:
        return render(request, "songs/login_register.html")


def center(request):
    return HttpResponse("Center")


def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("center"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        is_artist = False

        if "is_artist" in request.POST:
            is_artist = request.POST["is_artist"]
        
        if password != confirmation:
            return render(request, "network/login_register.html",  {
                "messages": "Passwords must match."
                })
        try:
            user = User.objects.create(username=username, email=email, password=password, is_artist=is_artist)
        except Exception as e:
            print(e)
            return render(request, "songs/login_register.html", {
                "message": str(e)
                #"message": "Username already taken."
                })
        login(request, user) 
        return HttpResponseRedirect(reverse("center"))
    else:
        return render(request, "songs/login_register.html")
