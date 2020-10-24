from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("rehome", views.rehome, name="rehome"),
    path("pet/<int:Id>", views.get_pet, name="pet"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("search", views.search, name="search"),
    path("logout", views.logout_view, name="logout"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
]
