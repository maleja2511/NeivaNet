from django.shortcuts import render
from .models import Notification

def get_notifications(request):
    user_notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    return render(request, 'notifications/notifications.html', {'notifications': user_notifications})



def notification_list(request):
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-date')
    return render(request, 'notifications/notification_list.html', {'notifications': user_notifications})
