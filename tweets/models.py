import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL
# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #delete default = 1 later. Code breaks if no default for some reason.
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

    class Meta:
        ordering = ['-id']
    
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 1000),
            "image": self.image.url if self.image else None
        }