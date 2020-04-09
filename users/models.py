from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
