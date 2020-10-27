
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>/newpost", views.newpost, name="newpost"),
    path("user/<str:username>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("like", views.like, name="like"),
    path("unlike", views.unlike, name="unlike")
]
