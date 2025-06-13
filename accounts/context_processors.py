from .models import Announcement, AnnouncementRead

def global_announcements(request):
    if not request.user.is_authenticated:
        return {}

    # Exclude announcements the user already read
    read_ids = AnnouncementRead.objects.filter(user=request.user).values_list('announcement_id', flat=True)

    announcements = Announcement.objects.filter(is_global=True).exclude(id__in=read_ids)

    user_announcements = Announcement.objects.filter(recipient=request.user).exclude(id__in=read_ids)

    all_announcements = (announcements | user_announcements).order_by('-created_at')

    return {
        'global_announcements': all_announcements
    }
