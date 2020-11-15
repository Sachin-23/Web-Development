
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("new_post", views.new_post, name="new_post"),
    path("get_post/<int:Id>", views.get_post, name="get_post"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("follow", views.follow, name="follow"),
    path("like", views.like, name="like"),
    path("profile/<str:username>", views.get_profile, name="get_profile"),
]
