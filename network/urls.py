
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API routes
    path("new_post", views.new_post, name="new_post"),
    path("user/<int:id>", views.view_profile, name="user"),
    path("following", views.following, name="following"),
    path("un_or_follow/<str:profile>", views.un_or_follow, name="un_or_follow"),
    path("un_or_like/<int:id>", views.un_or_like, name="un_or_like"),
    path("post/<int:id>", views.edit_post, name="edit")
]
