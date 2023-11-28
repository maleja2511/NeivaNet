import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.png')
    date_of_birth = models.DateField(null=True, blank=True)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    confirmation_sent_at = models.DateTimeField(default=timezone.now)

    def confirmation_token_expired(self):
        expiration_time = timezone.now() - timedelta(days=1)  # 1 día de validez, ajusta según necesites
        return self.confirmation_sent_at < expiration_time

    def __str__(self):
        return f'{self.user.username} Profile'
