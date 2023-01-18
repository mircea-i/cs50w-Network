from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

# Import models
from .models import User, Post, Follow, Like

# Import json
import json


def index(request):

    # Create pagination, split posts by 10 and order them
    p = Paginator(Post.objects.all().order_by("creation").reverse(), 10)

    # GET current page number
    p_number = request.GET.get("p_number")
    p_posts = p.get_page(p_number)

    # Try and get likes if user is logged in
    try:
        p_likes = Post.objects.filter(pk__in=Like.objects.filter(user=request.user).values_list('post'))
    except:
        ObjectDoesNotExist
        p_likes = []

    return render(request, "network/index.html", {'p_posts': p_posts, 'p_likes': p_likes})


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

    # Posting new post form
    if request.method == "POST":

        # Check if non empty post 
        if request.POST['post-content'] == "":
            return redirect(reverse("index"))

        # If all is ok then create new post
        else:
            Post.objects.create(
                owner = User.objects.get(pk=request.user.id),
                content = request.POST['post-content']
            )
            return redirect(reverse("index"))
    
    # Return to index 
    else:
        return redirect(reverse("index"))


@login_required
def view_profile(request, id):

    user_profile = User.objects.get(pk=id)

    # Check if viewing self profile and if following viewed profile
    my_profile = False
    is_following = False

    if request.user == user_profile:
        my_profile = True
    else:
        try:
            Follow.objects.get(user=user_profile, follower=request.user)
            is_following=True
        except:
            ObjectDoesNotExist

    p = Paginator(Post.objects.filter(owner__pk=id).order_by("creation").reverse(), 10)

    # Get liked posts
    try:
        p_likes = Post.objects.filter(pk__in=Like.objects.filter(user=request.user).values_list('post'))
    except:
        ObjectDoesNotExist
        p_likes = []

    # GET current page number
    p_number = request.GET.get("p_number")
    p_posts = p.get_page(p_number)

    #

    return render(request, "network/profile.html", {
        'p_posts': p_posts,
        'p_likes': p_likes,
        'followers': Follow.objects.filter(user=user_profile).count(),
        'following': Follow.objects.filter(follower=user_profile).count(),
        'my_profile': my_profile,
        'is_following': is_following,
        'user_profile': user_profile
        })


@login_required
def following(request):

    # Janky filter to get all followed users posts
    p = Paginator(Post.objects.filter(owner__pk__in=(Follow.objects.filter(follower=request.user).values_list('user'))).order_by("creation").reverse(), 10)
    
    # Try and get all likes
    try:
        p_likes = Post.objects.filter(pk__in=Like.objects.filter(user=request.user).values_list('post'))
    except:
        ObjectDoesNotExist
        p_likes = []
    
    # GET current page number
    p_number = request.GET.get("p_number")
    p_posts = p.get_page(p_number)
    return render(request, "network/index.html", {'p_posts': p_posts, 'p_likes': p_likes})


@login_required
def un_or_follow(request, profile):

    if request.method == "POST":

        # Try to delete follow relation if it exists and return to profile view
        try:
            Follow.objects.get(user=User.objects.get(username=profile), follower=request.user).delete()
            return HttpResponseRedirect(reverse(view_profile, kwargs={'id': User.objects.get(username=profile).pk}))
        except:
            ObjectDoesNotExist
        
        # Create follow relation if it does not exist and return to profile
        Follow.objects.create(user=User.objects.get(username=profile), follower=request.user)
        return HttpResponseRedirect(reverse(view_profile, kwargs={'id': User.objects.get(username=profile).pk}))
    
    # Go back to index if not using POST
    else:
        return HttpResponseRedirect(reverse(index))


@login_required
def edit_post(request, id):

    # Edit post content 
    if request.method == "POST":

        # Get data
        content = json.loads(request.body).get("body")

        if request.user == Post.objects.get(pk=id).owner:
            try:
                Post.objects.filter(pk=id).update(content=content)
                return JsonResponse({'content': content}, status=200)

            # Return to index if something went wrong
            except:
                ObjectDoesNotExist
                return HttpResponseRedirect(reverse(index))
        
        # Return to index if not post owner
        else:
            HttpResponseRedirect(reverse(index))

    # Return to index if reaching via GET
    else:
        return HttpResponseRedirect(reverse(index))


@login_required
def un_or_like(request, id):

    if request.method == "POST": 

        # Go back to index if trying to like own post
        if request.user == Post.objects.get(pk=id).owner:
            return redirect(reverse(index))
            
        content = json.loads(request.body).get("content")

        try:
            Like.objects.get(post__pk=id, user=request.user).delete()

            # F works only on filter, not on get; return current number of likes
            Post.objects.filter(pk=id).update(likes=F('likes') - 1)
            return JsonResponse({'data': Post.objects.get(pk=id).likes}, status=200)

        except:
            ObjectDoesNotExist
            Like.objects.create(post=Post.objects.get(pk=id), user=request.user)

            # F works only on filter, not on get; return current number of likes
            Post.objects.filter(pk=id).update(likes=F('likes') + 1)
            return JsonResponse({'data': Post.objects.get(pk=id).likes}, status=200)
