from django.urls import path
from .views import count_unread_notifications, get_notifications, notification_list

urlpatterns = [
    path('notifications/', get_notifications, name='get-notifications'),
    path('my-notifications/', notification_list, name='notification-list'),
    path('unread-notifications-count/', count_unread_notifications, name='unread-notifications-count'),
]