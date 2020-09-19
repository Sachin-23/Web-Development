from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.get, name="search"),
    path("wiki/<str:title>", views.get, name="search"),
    path("random/", views.random_page, name="random"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit"),
]
