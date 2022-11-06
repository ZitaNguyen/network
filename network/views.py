from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post
from .forms import NewPostForm


def index(request):
    posts = Post.objects.all().order_by('date_created').reverse()
    return render(request, "network/index.html", {
        'form': NewPostForm(),
        'posts': posts
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


@login_required
def add_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)

        if form.is_valid():
            content = request.POST['content']

            Post.objects.create(
                poster = request.user,
                content = content
            )

        return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request, poster_name):
    poster_id = User.objects.filter(username=poster_name).first()
    posts = Post.objects.filter(poster=poster_id).order_by('date_created').reverse()
    return render(request, "network/profile.html", {
        'posts': posts,
        'poster': poster_name
    })