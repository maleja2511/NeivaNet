from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    date_of_birth = models.DateField(null=True, blank=True)

    def _str_(self):
        return f'{self.user.username} Profile'