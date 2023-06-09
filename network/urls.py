
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("toggle_like/<int:post_id>", views.toggle_like, name="toggle_like"),
    path("profile/<str:poster_name>", views.profile, name="profile"),
    path("profile/<str:poster_name>/toggle_follow", views.toggle_follow, name="toggle_follow"),
    path("following", views.following, name="following"),
]
