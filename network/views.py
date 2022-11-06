from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post, FollowList
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
    try:
        follow_list = FollowList.objects.get(user=request.user)
    except FollowList.DoesNotExist:
        follow_list = None

    return render(request, "network/profile.html", {
        'posts': posts,
        'poster': poster_name,
        'follow_list': follow_list
    })


@login_required
def toggle_follow(request, poster_name):
    if request.method == "POST":
        poster = User.objects.filter(username=poster_name).first()

        # Manage following list: user=request.user, FollowList.followings=poster
        try:
            user_following_list = FollowList.objects.get(user=request.user)
        except FollowList.DoesNotExist:
            user_following_list = None

        if user_following_list is None:
            user_following_list = FollowList.objects.create(user=request.user)
            user_following_list.followings.add(poster)
            user_following_list.save()

        elif poster not in user_following_list.followings.all():
            user_following_list.followings.add(poster)
            user_following_list.save()

        else:
            user_following_list.followings.remove(poster)
            user_following_list.save()

        # Manage follower list: user=poster, FollowList.followers:request.user
        try:
            user_follower_list = FollowList.objects.get(user=poster)
        except FollowList.DoesNotExist:
            user_follower_list = None

        if user_follower_list is None:
            user_follower_list = FollowList.objects.create(user=poster)
            user_follower_list.followers.add(request.user)
            user_follower_list.save()

        elif request.user not in user_follower_list.followers.all():
            user_follower_list.followers.add(request.user)
            user_follower_list.save()

        else:
            user_follower_list.followers.remove(request.user)
            user_follower_list.save()

    return redirect('profile', poster_name=poster_name)