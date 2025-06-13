from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'is_global', 'created_at', 'is_read')
    list_filter = ('is_global', 'is_read')
    search_fields = ('title', 'body')
