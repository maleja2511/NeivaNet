from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.posts, name="posts"),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
]