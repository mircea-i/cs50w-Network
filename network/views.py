from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post

import json

from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone


def index(request):
    return render(request, "network/index.html")


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
def new_post(request):

    if request.method == "POST":
        data = json.loads(request.body)
        print (data)
        Post.objects.create(
            owner = User.objects.get(username=request.user),
            content = data.get("content", ""),
            creation = timezone.now(),
            likes = 0
            )

        print (request.user, data.get("content"))
    
        return JsonResponse({"message": "Email sent successfully."}, status=201)


def posts(request):
    all_posts = Post.objects.all().order_by("-creation")
    # print ([post.serialize() for post in all_posts])
    return JsonResponse([post.serialize() for post in all_posts], safe=False)
    