from django.contrib import admin
from .models import Profile, Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'is_global', 'created_at', 'is_read')
    list_filter = ('is_global', 'is_read')
    search_fields = ('title', 'body')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_location', 'motto')
    search_fields = ('user__username', 'current_location', 'motto')
