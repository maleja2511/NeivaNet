from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.posts, name="posts"),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("delete_reply/<int:reply_id>/", views.delete_reply, name="delete_reply"),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
]