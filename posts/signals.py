from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import render
from .models import Post, Like, Comment
from notifications.models import Notification
from django.db.models.signals import post_save

@receiver(post_save, sender=Post)
def create_post_notification(sender, instance, created, **kwargs):
    if created:
        all_users = User.objects.exclude(id=instance.author.id)
        for user in all_users:
            Notification.objects.create(
                recipient=user,
                sender=instance.author,
                post=instance,
                type=Notification.POSTED,
                text=f'{instance.author.username} ha publicado una nueva entrada: {instance.title}',
                link=f'/my-notifications/'
            )

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.user,
            post=instance.post,
            type=Notification.LIKED,
            text=f'{instance.user.username} le ha dado me gusta a tu publicación: {instance.post.title}',
            link=f'/my-notifications/'
        )
        
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.parent is None:  # Asegúrate de que es un comentario y no una respuesta
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.user,
            post=instance.post,
            type=Notification.COMMENTED,
            text=f'{instance.user.username} ha comentado en tu publicación: {instance.post.title}',
            link=f'/my-notifications/'
        )

@receiver(post_save, sender=Comment)
def create_reply_notification(sender, instance, created, **kwargs):
    if created and instance.parent is not None:  # Asegúrate de que es una respuesta
        Notification.objects.create(
            recipient=instance.parent.user,
            sender=instance.user,
            post=instance.post,
            type=Notification.REPLIED,
            text=f'{instance.user.username} ha respondido a tu comentario en la publicación: {instance.post.title}',
            link=f'/my-notifications/'
        )
