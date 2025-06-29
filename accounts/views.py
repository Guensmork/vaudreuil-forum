from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from django.contrib.auth.models import User
from .models import Profile, Announcement, AnnouncementRead
from forum.models import Thread, Post

from .forms import RegistrationForm, UserForm, ProfileForm


@login_required
def dashboard_view(request):
    my_threads = request.user.forum_threads.order_by('-created_at')[:5]
    my_posts = request.user.forum_posts.order_by('-created_at')[:5]

    read_ids = AnnouncementRead.objects.filter(user=request.user).values_list('announcement_id', flat=True)
    announcements = (Announcement.objects.filter(is_global=True) |
                     Announcement.objects.filter(recipient=request.user)).exclude(id__in=read_ids).order_by('-created_at')

    return render(request, 'accounts/dashboard.html', {
        'my_threads': my_threads,
        'my_posts': my_posts,
        'announcements': announcements,
    })


@require_POST
@login_required
def mark_announcement_read(request, announcement_id):
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        AnnouncementRead.objects.get_or_create(user=request.user, announcement=announcement)
        return JsonResponse({'status': 'ok'})
    except Announcement.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)


class LogoutView(BaseLogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def register(request):
    if request.user.is_authenticated:
        return redirect('forum:index')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('forum:index')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def community_directory(request):
    users = User.objects.all().order_by('username')
    return render(request, 'accounts/community_directory.html', {
        'users': users,
    })


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')  # update URL name if different
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



@login_required
def profile_view(request):
    Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

from django.contrib.auth.decorators import login_required

@login_required
def debug_profile_view(request):
    return render(request, 'accounts/debug_profile.html')


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile_detail.html', {'user': user})