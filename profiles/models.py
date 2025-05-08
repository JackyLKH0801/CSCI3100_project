from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
User = settings.AUTH_USER_MODEL

class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #user who is following
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE) #user who is being followed
    timestamp = models.DateTimeField(auto_now_add=True) #timestamp of when the user started following the profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=220, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True) #many to many relationship with user model. A user can have many followers and a follower can follow many users.
    timestamp = models.DateTimeField(auto_now_add=True) #timestamp of when the profile was created
    updated = models.DateTimeField(auto_now=True) #timestamp of when the profile was updated
def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    
post_save.connect(user_did_save, sender=User)
#when a user is created, create a profile for them. This is a signal that listens for the post_save signal from the User model. When a user is created, it calls the user_did_save function which creates a profile for the user.