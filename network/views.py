from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .models import User, Post, Profile

class PostForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={"rows":2}), max_length=300, required=True)

def index(request):
    posts_list = Post.objects.all().order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/index.html", {
        'form': PostForm(),
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
        profile = Profile()
        profile.user = user
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newpost(request, username):
    if request.method == 'POST':
        text = request.POST.get("text")
        user = get_object_or_404(User, username=username)
        post = Post.objects.create(text=text, user=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return render(request, "network/error.html", {
            'error': "The profile you requested does not exist."
        })
    user_profile = Profile.objects.get(user=user)
    followers = user_profile.follower.all()
    following = user_profile.following.all()
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    return render(request, "network/profile.html", {
        'user': user,
        'user_profile': user_profile,
        'posts': posts,
        'followers': followers,
        'following': following
    })

@csrf_exempt
def follow(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        user = User.objects.get(username=user)
        profile = Profile.objects.get(user=request.user)
        profile.following.add(user)
        profile.save()
        profile = Profile.objects.get(user=user)
        profile.follower.add(request.user)
        profile.save()
        return JsonResponse({}, status=201)

@csrf_exempt
def unfollow(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        user = User.objects.get(username=user)
        profile = Profile.objects.get(user=request.user)
        profile.following.remove(user)
        profile.save()
        profile = Profile.objects.get(user=user)
        profile.follower.remove(request.user)
        profile.save()
        return JsonResponse({}, status=201)

@login_required
def following(request):
    posts_following = []
    user_following = Profile.objects.filter(follower=request.user)
    posts_list = Post.objects.all().order_by('-timestamp')
    for post in posts_list:
        for following in user_following:
            if following.user == post.user:
                posts_following.append(post)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_following, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/index.html", {
        'form': PostForm(),
        'posts': posts
    })

@csrf_exempt
def edit_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_content = request.POST.get('post_content')
        post = Post.objects.get(id=post_id)
        post.text = post_content
        post.save()
        return JsonResponse({}, status=201)

@csrf_exempt
def like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        post.likes.add(request.user)
        post.save()
        return JsonResponse({}, status=201)

@csrf_exempt
def unlike(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        post.likes.remove(request.user)
        post.save()
        return JsonResponse({}, status=201)
