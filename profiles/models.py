from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
import uuid

User = settings.AUTH_USER_MODEL

class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #user who is following
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE) #user who is being followed
    timestamp = models.DateTimeField(auto_now_add=True) #timestamp of when the user started following the profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) #unique license for the profile
    real_license = models.CharField(max_length=19, unique=True, editable=False)
    license_active = models.BooleanField(default=False)
    location = models.CharField(max_length=220, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True) #many to many relationship with user model. A user can have many followers and a follower can follow many users.
    timestamp = models.DateTimeField(auto_now_add=True) #timestamp of when the profile was created
    updated = models.DateTimeField(auto_now=True) #timestamp of when the profile was updated
    def generate_license_key(self):
        raw_uuid = uuid.uuid4().hex  # Get 32-character hex string
        formatted = f"{raw_uuid[:4]}-{raw_uuid[4:8]}-{raw_uuid[8:12]}-{raw_uuid[12:16]}"
        return formatted.upper()
    def save(self, *args, **kwargs):
    #   """Override save to ensure license key exists"""
        self.real_license = self.generate_license_key()
        super().save(*args, **kwargs)
def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    
post_save.connect(user_did_save, sender=User)
#when a user is created, create a profile for them. This is a signal that listens for the post_save signal from the User model. When a user is created, it calls the user_did_save function which creates a profile for the user.