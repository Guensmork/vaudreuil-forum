from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

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



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts_threads')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('category', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts_posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} on {self.thread.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
