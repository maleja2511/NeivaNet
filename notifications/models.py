from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    POSTED = 'posted'
    LIKED = 'liked'
    COMMENTED = 'commented'
    REPLIED = 'replied'
    NOTIFICATION_TYPES = [
        (POSTED, 'Posted'),
        (LIKED, 'Liked'),
        (COMMENTED, 'Commented'),
        (REPLIED, 'Replied'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey('posts.Post', on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    text = models.TextField(null=True)
    link = models.URLField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.recipient.username} - {self.type}'

