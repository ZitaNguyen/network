import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, FollowList
from .forms import NewPostForm


def index(request):
    posts = Post.objects.all().order_by('date_created').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        'page_obj': page_obj
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

        return redirect('profile', poster_name=request.user.username)


@login_required
def profile(request, poster_name):
    poster_id = User.objects.filter(username=poster_name).first()
    posts = Post.objects.filter(poster=poster_id).order_by('date_created').reverse()
    try:
        follow_list = FollowList.objects.get(user=request.user)
    except FollowList.DoesNotExist:
        follow_list = None
    try:
        poster_follow_list = FollowList.objects.get(user=poster_id)
    except FollowList.DoesNotExist:
        poster_follow_list = None

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        'poster_id': poster_id,
        'page_obj': page_obj,
        'poster': poster_name,
        'follow_list': follow_list,
        'poster_follow_list': poster_follow_list,
        'form': NewPostForm()
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


@login_required
def following(request):
    all_posts = []
    try:
        follow_list = FollowList.objects.get(user=request.user)
    except FollowList.DoesNotExist:
        follow_list = None

    if follow_list is None or follow_list.followings.all() is None:
        all_posts = []
    else:
        followings = follow_list.followings.all()

        for following in followings:
            posts = Post.objects.filter(poster=following)
            for post in posts:
                all_posts.append(post)

    all_posts.sort(key=lambda x: x.date_created, reverse=True)
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        'page_obj': page_obj
    })


@csrf_exempt
@login_required
def edit_post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    # Update post content
    if request.method == "PUT":
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)


@csrf_exempt
@login_required
def toggle_like(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    # Update post content
    if request.method == "PUT":
        fan = post.fan.all()
        # if user haven't liked the post
        if fan is None or request.user not in fan:
            # like post
            post.fan.add(request.user)
            post.save()
        else:
            # unlike post
            post.fan.remove(request.user)
            post.save()
        return HttpResponse(status=204)
