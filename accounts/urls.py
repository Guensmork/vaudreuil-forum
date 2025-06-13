from django.urls import path
from . import views
from .views import register
from .views import dashboard_view

app_name = 'accounts'

urlpatterns = [
    # existing paths like 'login/', 'logout/', etc.
    path('register/', register, name='register'),
    path('users/<str:username>/', views.profile_detail, name='profile_detail'),
    path('members/', views.community_directory, name='community_directory'),
    path('announcements/read/<int:announcement_id>/', views.mark_announcement_read, name='mark_announcement_read'),

]


urlpatterns += [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]


urlpatterns += [
    path('dashboard/', dashboard_view, name='dashboard'),
    
]
