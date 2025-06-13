from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from forum.models import Thread, Post
from django.contrib.auth import login
from .forms import RegistrationForm
from accounts.models import Announcement
from django.http import JsonResponse
from .models import Announcement, AnnouncementRead
from django.views.decorators.http import require_POST



def register(request):
    if request.user.is_authenticated:
        return redirect('forum:index')  # Already logged in? Redirect.

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log them in after signup
            return redirect('forum:index')  # Redirect after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def community_directory(request):
    users = User.objects.all().order_by('username')  # Or order by date_joined, etc.
    return render(request, 'accounts/community_directory.html', {
        'users': users,
    })


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    threads = user.forum_threads.order_by('-created_at')
    posts = user.forum_posts.order_by('-created_at')
    profile = getattr(user, 'profile', None)

    announcements = Announcement.objects.filter(is_global=True)

    if request.user.is_authenticated:
        user_specific = Announcement.objects.filter(recipient=request.user)
        announcements = (announcements | user_specific).order_by('-created_at')

    return render(request, 'accounts/profile_detail.html', {
        'profile_user': user,
        'profile': profile,
        'threads': threads,
        'posts': posts,
        'announcements': announcements,
    })



@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@require_POST
@login_required
def mark_announcement_read(request, announcement_id):
    try:
        announcement = Announcement.objects.get(id=announcement_id)

        # Create read record if not already exists
        AnnouncementRead.objects.get_or_create(user=request.user, announcement=announcement)

        return JsonResponse({'status': 'ok'})
    except Announcement.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)


from django.contrib.auth.decorators import login_required
from forum.models import Thread, Post
from .models import Announcement, AnnouncementRead

@login_required
def dashboard_view(request):
    # Latest threads/posts by the user
    my_threads = request.user.forum_threads.order_by('-created_at')[:5]
    my_posts = request.user.forum_posts.order_by('-created_at')[:5]

    # Unread announcements
    read_ids = AnnouncementRead.objects.filter(user=request.user).values_list('announcement_id', flat=True)
    announcements = (Announcement.objects.filter(is_global=True) | 
                     Announcement.objects.filter(recipient=request.user)).exclude(id__in=read_ids).order_by('-created_at')

    return render(request, 'accounts/dashboard.html', {
        'my_threads': my_threads,
        'my_posts': my_posts,
        'announcements': announcements,
    })
