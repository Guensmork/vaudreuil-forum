from django.urls import path
from . import views
from .views import register
from .views import dashboard_view

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('users/<str:username>/', views.profile_detail, name='profile_detail'),
    path('members/', views.community_directory, name='community_directory'),
    path('register/', register, name='register'),
    path('announcements/read/<int:announcement_id>/', views.mark_announcement_read, name='mark_announcement_read'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('debug-profile/', views.debug_profile_view, name='debug_profile'),

]


urlpatterns += [
    path('edit/', views.edit_profile, name='edit_profile'),
    path('users/<str:username>/', views.profile_detail, name='profile_detail'),
]


