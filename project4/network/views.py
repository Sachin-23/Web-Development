import json
import time
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    all_posts = Post.objects.all()

    p = Paginator(all_posts, 10)

    # get current_page
    current_page =  int(request.GET.get("page") or 1)

    page = p.page(current_page)

    page_range = p.page_range

    liked = False

    if request.user.username:
        current_user = User.objects.get(username=request.user.username)
   
    liked_user = []
    if request.user.username != "":
        for i in page:
            if current_user in [j.user for j in Like.objects.filter(user=current_user, post=i)]:
                liked_user.append(True)
            else:
                liked_user.append(False)


    if len(liked_user) == 0:
        liked_user = [False] * 10;

    return render(request, "network/index.html",  {
        "username": request.user.username,
        "posts": zip(page, liked_user),
        "prev": page.has_previous(),
        "next": page.has_next(),
        "current_page": current_page,
        "range": max(page_range)
        })

def new_post(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        content = request.POST["content"]
        new_post = Post(user=user, body=content)
        new_post.save()         
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/error.html", {
            "msg": f"Username with '{username}' does not exist"
            })

@login_required(login_url="login")
def like(request):
    if request.method != "PUT":
        return JsonResponse({"msg": "Only put request is allowed."}, status=405)
    else:
        try:
            if request.user.is_authenticated: 
                data = json.loads(request.body)
                Id = data["id"]
                action = data["action"]
                post = Post.objects.get(id=Id)
                if action == "like":
                    post.likes += 1
                    like = Like(user=request.user, post=post)
                    like.save()
                    post.save()
                else:
                    post.likes -= 1
                    like = Like.objects.get(user=request.user, post=post)
                    like.delete()
                    post.save()
                return JsonResponse({"msg": "Successfully Edited."}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"msg": "Not authorized."}, status=500)

def get_profile(request, username):

    # testing purpose
    # remove this 
    # return HttpResponse(username)

    current_user = User(username=request.user.username)

    follows = False

    # get user object 
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        print(e)
        return render(request, "network/error.html", {
            "msg": f"Username with '{username}' does not exist"
            })

    # get post in reverse chronological order
    posts = Post.objects.filter(user=user)

    # 
    p = Paginator(posts, 10)
    
    current_page =  int(request.GET.get("page") or 1)

    page = p.page(current_page)

    page_range = p.page_range

    # get followers
    followers = Follower.objects.filter(user=user)
    
    liked_user = []
    if request.user.username != "":
        for i in page:
            if current_user in [j.user for j in Like.objects.filter(user=current_user, post=i)]:
                liked_user.append(True)
            else:
                liked_user.append(False)


    if len(liked_user) == 0:
        liked_user = [False] * 10;


    if str(current_user) in [i.follower.username for i in followers]:
        follows = True

    # get following 
    following = Follower.objects.filter(follower=user)


    return render(request, "network/profile.html", {
            "username": username, 
            "posts": zip(page, liked_user),
            "prev": page.has_previous(),
            "next": page.has_next(),
            "followers": followers,
            "following": following,
            "follows": follows,
            "current_page": current_page,
            "range": max(page_range)
            })

@login_required(login_url="/login")
def follow(request):
    if request.method == "POST":
        current_user = User.objects.get(username=request.user.username)

        data = json.loads(request.body)

        req_user = User.objects.get(username=data["username"]) 

        followers = Follower.objects.filter(user=req_user)

        if data["action"] == "Follow" and current_user not in followers:
            print("followed")
            f = Follower(user=req_user, follower=current_user)
            f.save()
        elif data["action"] == "Unfollow":
            print("Unfollowed")
            f = Follower.objects.get(user=req_user, follower=current_user)
            f.delete()
        else: 
            return JsonResponse({"error": "error occurred"}, status=400)
        return JsonResponse({"msg": "success"}, status=200)
    else:
        return JsonResponse({"error": "error occurred"}, status=400)


def get_post(request, Id):
    try: 
        post = Post.objects.get(id=Id)
    except Exception as e:
        print(e)
        return JsonResponse({ "msg": f"Post does not exist"})
    return JsonResponse(post.serialize(), status=200)



@login_required(login_url="/login")
def edit_post(request):
    if request.method != "POST":
        return JsonResponse({"msg": "Only post request is allowed."}, status=405)
    else:
        data = json.loads(request.body)
        Id = data["id"]
        post = Post.objects.get(id=Id)
        if request.user.username == post.user.username:
            content = data["content"]
            post.body = content
            post.save()
            return JsonResponse({"msg": "Successfully Edited."}, status=200)
        else:
            return HttpResponseRedirect(reverse("get_profile", args=[post.user.username]))



@login_required(login_url="/login")
def following(request):

    current_page = 0

    current_user = User.objects.get(username=request.user.username)

    # get the following users list 
    following = Follower.objects.filter(user=current_user)

    # get all posts, posted by the followers list
    posts = []

    for user in following:
        posts += Post.objects.filter(user=user.follower)

    p = Paginator(posts, 10)
    
    page_range = p.page_range

    current_page = int(request.GET.get("page") or 1)

    page = p.page(current_page)

    liked_user = []
    if request.user.username != "":
        for i in page:
            if current_user in [j.user for j in Like.objects.filter(user=current_user, post=i)]:
                liked_user.append(True)
            else:
                liked_user.append(False)


    if len(liked_user) == 0:
        liked_user = [False] * 10;

    return render(request, "network/following.html",  {
        "username": request.user.username,
        "prev": page.has_previous(),
        "next": page.has_next(),
        "posts": zip(page, liked_user),
        "current_page": current_page,
        "range": max(page_range)
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
