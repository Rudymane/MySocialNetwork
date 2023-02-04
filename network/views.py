import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import os

from .models import User, Posts, Liked, Following, Profiles, Banners
from .forms import ImageForm, BannerForm


def index(request):
    if request.user.is_authenticated:
        image = User.objects.get(pk= request.user.id)
        followcount = Following.objects.all()
        followerslist=[]
        followers=[post.serialize()for post in followcount]
       
        following = Following.objects.filter(user_id= image.id)

        for i in followers:
            followerslist.append(i['user_id'])


        
        return render(request, "network/index.html",{
            "profile_name": image.username,
            "images" : image.image,
            "followers" : followerslist.count([request.user.id]),
            "following" : len(following)
        })
    else:
        return render(request, "network/index.html")

# returns profile page of requested user
def profile(request, profile):
    image = User.objects.get(username= profile)
    followcount = Following.objects.all()
    followerslist=[]
    followers=[post.serialize()for post in followcount]
    following = Following.objects.filter(user_id= image.id)

    for i in followers:
            followerslist.append(i['user_id'])
    
    return render(request, "network/profile.html",{
        "profile_name": profile,
        "images" : image.image,
        "banners": image.banner,
        "followers" : followerslist.count([image.id]),
        "following" : len(following)
    })

@login_required
# retrieves information about whether a post is liked and returns Posts information
def comments(request, post_id):
    posts = Posts.objects.get(pk=post_id)
    user_likes = [liked.user_id for liked in posts.user_likes.all()]
    if request.user.id in user_likes:
        color = "aqua"
    else:
        color = "black"
    
    return render(request, "network/comments.html", {
        "id": posts.id,
        "poster_id": posts.user.id,
        "username": posts.user.username,
        "body": posts.body,
        "timestamp": posts.timestamp.strftime("%b %d, %Y, %I:%M %p"),
        "likes": posts.likes,
        "color": color,
        "users_id": request.user.id,
        "profile": str(posts.user.image),
    })


def user_follows(request):
    return render(request, "network/following.html")

# upload takes the user submitted image files and saves it to the User database table
def upload(request):
	if request.method == "POST":
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			
			form.save()
			old_image= Profiles.objects.filter(user_profile_id=request.user.id).values_list('image', flat=True)
                        
            # delete older image if it exists
			if len(old_image) > 1:
				Profiles.objects.filter(user_profile_id=request.user.id)[0].delete()
				os.remove(old_image[0])
			
				User.objects.filter(pk=request.user.id).update(image = old_image[1])
			else:
				User.objects.filter(pk=request.user.id).update(image = old_image[0])
			

			return render(request, "network/settings.html", {'id': request.user.id})
	

	return render(request, "network/settings.html", {'id': request.user})

def banner_upload(request):
	if request.method == "POST":
		form = BannerForm(request.POST, request.FILES)
		if form.is_valid():
			# save form and create model row in profile
			form.save()
            # get paths of images the user has uploaded (that's what the values_list portion does)
			old_image= Banners.objects.filter(user_profile_id=request.user.id).values_list('banner', flat=True)

			if len(old_image) > 1:
				Banners.objects.filter(user_profile_id=request.user.id)[0].delete()
				os.remove(old_image[0])
				
				User.objects.filter(pk=request.user.id).update(banner = old_image[1])
			else:
				User.objects.filter(pk=request.user.id).update(banner = old_image[0])
			

			return render(request, "network/settings.html", {'id': request.user.id})
	

	return render(request, "network/settings.html", {'id': request.user})

def settings(request):
    return render(request, "network/settings.html", {'id': request.user.id})

def settings_banner(request):
    return render(request, "network/settings_banner.html", {'id': request.user.id})

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

@csrf_exempt
@login_required
# loads info sent from javascript and saves the post in the Posts table
def newpost(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    body = data.get("body", "")
    post = Posts(
        parent= 0,
        user=request.user,
        body=body
    )
    post.save()
    return JsonResponse({"message": "Post Successful"}, status=201)

@csrf_exempt
@login_required
# loads info sent from javascript and saves the comments in the Posts table
def newcomment(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    body = data.get("body", "")
    parent_id = data.get("parent","")
    post = Posts(
        parent = parent_id,
        user=request.user,
        body=body
    )
    post.save()
    return JsonResponse({"message": "Post Successful"}, status=201)

@csrf_exempt
@login_required
# saves the edited post into the Posts table
def edit(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    body = data.get("body", "")
    post = Posts.objects.get(pk=post_id)
    post.body = body
    post.save()
    

    return JsonResponse({"message": "Post Successful"}, status=201)

@csrf_exempt
@login_required
# adds or removes likes from the Liked table
def liked(request, post_id):
    
    like = Posts.objects.get(pk=post_id)
    if request.method == "PUT":
        # data.get("like") will equal aqua if a post has been liked. 
        data = json.loads(request.body)
        if data.get("like") == "aqua":
           
            user_likes = Liked(
                user=request.user,
                post= Posts.objects.get(pk=post_id)
            )
            
            user_likes.save()
            like.likes +=1
            like.save()
            like.user_likes.add(user_likes) 
        else:
            user_likes = Liked.objects.get(user = request.user, post= Posts.objects.get(pk=post_id) )
            like.likes -=1
            like.save()
            user_likes.delete()
            
    return HttpResponse(status=204)

# following() updates the database on whether the user just followed or unfollowed someone.
@csrf_exempt
@login_required
def following(request, name):
       
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("follow") == "Followed":
            follows  = Following(
                user=request.user,
                
            )
            follows.save()
            follows.followed.add(User.objects.get(username=name))
        else:
            follows = Following.objects.get(user = request.user, followed = User.objects.get(username=name))
            follows.delete()
            
    return HttpResponse(status=204)

# Function returns javascript data on whether or not a person is followed
@login_required
def followfeed(request):
   
    follow = Following.objects.filter(user_id = request.user)
    return JsonResponse([follow.serialize() for follow in follow], safe=False)


# Feed sorts the list of people/posts
@login_required
def feed(request):
    # parent_id is essential for determining if a post is a comment or an original post
    parent_id = str(request.GET.get("parent"))
    usersname = str(request.GET.get("username"))
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))
    # If username is empty, we can return all the posts. Else, we return the posts made by the person who's profile we must be on.
    if usersname == "":
        posts = Posts.objects.filter(parent = parent_id)
        feed = posts.order_by('-timestamp').all()
        feed = feed[start:end +1]
        return JsonResponse([post.serialize(int(request.user.id)) for post in feed], safe=False)

    if usersname == "Following":
        postslist = []
        posts = Following.objects.filter(user_id = request.user )
        for i in posts:
            postslist += i.serialize()["user_id"]

        posts = Posts.objects.filter(user_id__in =postslist , parent = parent_id)
    else:
        theuser = User.objects.get(username = usersname)
        posts = Posts.objects.filter(user_id = theuser.id, parent = parent_id)

    feed = posts.order_by('-timestamp').all()
    feed = feed[start:end +1]
    return JsonResponse([post.serialize(int(request.user.id)) for post in feed], safe=False)

# search() allows you search for a user using the search bar
def search(request):
    people = []
    for i in User.objects.all():
        people.append(i.username)
    return JsonResponse(people, safe=False)

