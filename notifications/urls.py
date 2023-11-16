from django.urls import path
from .views import get_notifications, notification_list

urlpatterns = [
    path('notifications/', get_notifications, name='get-notifications'),
    path('my-notifications/', notification_list, name='notification-list'),
]