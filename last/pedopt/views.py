from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django import forms 
import json
import re


class AddPet(forms.ModelForm):
    class Meta:
        model = Pet 
        fields = ('name', 'image', 'age_group', 'sex','zip_code', 'city', 'state', 'pet_type', 'about')
        widgets = {
                'name': forms.TextInput(attrs={"placeholder": "Ginger", "class": "form-control"}),
                "image": forms.FileInput(attrs={"class": "form-control-file"}),
                'Age': forms.Select(attrs={"class": "form-control"}),
                'sex': forms.Select(attrs={"class": "form-control"}),
                'zip_code': forms.NumberInput(attrs={"placeholder": "400001", "class": "form-control", "pattern": "[0-9]{6}"}),
                'city': forms.TextInput(attrs={"class": "form-control"}),
                'state': forms.TextInput(attrs={"class": "form-control"}),
                'pet_type': forms.Select(attrs={"class": "form-control"}),
                'about': forms.Textarea(attrs={"placeholder": "Pet's Liking, Type of Home needed, About Pet.", "class": "form-control", "rows": "5"})
                }


def index(request):
    pets = Pet.objects.all()
    return render(request, "pedopt/index.html", {
        "pets": pets
        })

@login_required
def get_pet(request, Id):
    message = ""
    try:
        pet = Pet.objects.get(id=Id)
        wishlist = Wishlist.objects.filter(user=request.user, pet=pet)
        return render(request, "pedopt/get_pet.html",  {
            "pet": pet,
            "wishlist": wishlist
            })
    except Exception as e:
        print(e)
        return render(request, "pedopt/get_pet.html",  {
            "message": "Sorry, this page isn't available."
            })

@login_required
def wishlist(request):
    if request.method == "PUT":
        if request.user.is_authenticated:
            print("Got put request")
            data = json.loads(request.body)
            Id = data["id"]
            try:
                pet = Pet.objects.get(id=Id)
                wishlist = Wishlist.objects.filter(user=request.user, pet=pet)
                if len(wishlist) > 0:
                    wishlist[0].delete()
                else:
                    wishlist = Wishlist(user=request.user, pet=pet)
                    wishlist.save()
                return JsonResponse({"message": "Success.", "status": 200}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({"message": "Internal server error."}, status=500)
    else:
        return JsonResponse({"message": "Not authorized."}, status=500)


def search(request):
    location = request.GET["location"]
    pet_type = request.GET["type"]
    age = request.GET["age"]
    sex = request.GET["sex"]
    print(location, pet_type, age, sex)
    if location.isdecimal():
        pets = Pet.objects.filter(zip_code=int(location), pet_type=pet_type, \
                age_group=age, sex=sex)
    else:
        p = r"\w+"
        location = re.findall(p, location)
        if len(location) > 2:
            pets = Pet.objects.filter(city=location[0], state=location[1], \
                    pet_type=pet_type, age_group=age, sex=sex)
        else:
            pets = Pet.objects.filter(city=location[0], pet_type=pet_type, \
                    age_group=age, sex=sex)
    print(pets)
    return render(request, "pedopt/index.html", {
        "pets": pets
        })

@login_required
def rehome(request):
    if request.method == "POST":
        form = AddPet(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user
            pet.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "pedopt/rehome.html", {
                "message": "Please try again.",
                "form": form or AddPet()
            })
    return render(request, "pedopt/rehome.html", {
        "form": AddPet()
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"] 
        password = request.POST["password"] 
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "pedopt/login.html", {
                "message": "Invalid username and/or password."
                })
    return render(request, "pedopt/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "pedopt/register.html",  {
                "message": "Passwords must match."
                })
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(request, "pedopt/register.html", {
                "message": "Username already taken."
                })
    return render(request, "pedopt/register.html")
