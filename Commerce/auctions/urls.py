from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<str:name>", views.get_listing, name="listing"),
    path("closed/", views.show_closed_listing, name="closed"),
    path("create/", views.create_listing, name="create_listing"),
    path("watchlist/", views.get_watchlist, name="watchlist"),
    path("category/", views.get_category, name="category"),
    path("category/<str:category>", views.get_category, name="category")
]
