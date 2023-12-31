from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def get_notifications(request):
    user_notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    for notification in user_notifications:
        notification.is_read = True
        notification.save()
    return render(request, 'notifications/notifications.html', {'notifications': user_notifications})

@login_required
def notification_list(request):
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-date')
    return render(request, 'notifications/notification_list.html', {'notifications': user_notifications})

def count_unread_notifications(request):
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})
