from django.db import models
from django.conf import settings

class Notification(models.Model):
    # Tipo de notificación (por ejemplo, nueva publicación, respuesta, etc.)
    type = models.CharField(max_length=100)
    # Usuario que recibe la notificación
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    # Usuario que genera la notificación
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.CASCADE)
    # Texto de la notificación
    text = models.TextField()
    # Fecha y hora de creación
    created_at = models.DateTimeField(auto_now_add=True)
    # Si la notificación ha sido leída
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.to_user.username}'
