from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(default='network/files/userimages/default-avatar.jpg', blank=True)
    banner = models.ImageField(default='network/files/userimages/krgq9kqlgbk71.png', blank=True)

# creates a table for all posts and comments
class Posts(models.Model):
    parent = models.IntegerField(default=0)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    user_likes = models.ManyToManyField("Liked", related_name="user_liked")


    def serialize(self, users_id):
        
        return{
            "id": self.id,
            "poster_id": self.user.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d, %Y, %I:%M %p"),
            "likes": self.likes,
            "user_likes": [liked.user_id for liked in self.user_likes.all()],
            "users_id": users_id,
            "profile": str(self.user.image),
        }

# creates table of liked posts        
class Liked(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="their_likes")
    post = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name="post_liked")

# stores info of who is following who
class Following(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower")
    followed = models.ManyToManyField("User", related_name="thefollowed")

    def serialize(self):

        return{
            "name": [thefollowed.username for thefollowed in self.followed.all()],
            "user_id": [thefollowed.id for thefollowed in self.followed.all()]
        }

# The Comments class is going to be the same as the Posts class, but with the id of the Posts class to sort comments by.

# keeps information for user's profile image
class Profiles(models.Model):
    user_profile = models.ForeignKey("User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to= 'network/files/userimages')

# keeps information for user's banner image    
class Banners(models.Model):
    user_profile = models.ForeignKey("User", on_delete=models.CASCADE)
    banner = models.ImageField(upload_to= 'network/files/userimages')