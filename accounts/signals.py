from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from .models import Profile

@receiver(post_save, sender=User)
def create_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(user_logged_in)
def create_profile_on_login(sender, user, request, **kwargs):
    Profile.objects.get_or_create(user=user)
