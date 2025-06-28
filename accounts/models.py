from PIL import Image
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField("About Me", blank=True)
    website = models.URLField("Website or Portfolio", blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    current_location = models.CharField("Where I'm participating from", max_length=100, blank=True)
    motto = models.CharField("My Motto", max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            avatar_path = self.avatar.path
            img = Image.open(avatar_path)

            max_size = (300, 300)  # Change to whatever standard you prefer

            img.thumbnail(max_size, Image.LANCZOS)
            img.save(avatar_path)


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    is_global = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)  # Per user if needed

    def __str__(self):
        return self.title


class AnnouncementRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'announcement')
