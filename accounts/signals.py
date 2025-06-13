from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# Create profile when a new user is saved
@receiver(post_save, sender=User)
def create_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Ensure profile exists when a user logs in
@receiver(user_logged_in)
def create_profile_on_login(sender, user, request, **kwargs):
    Profile.objects.get_or_create(user=user)
