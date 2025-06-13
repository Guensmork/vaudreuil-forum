from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_index, name='index'),
    path('<slug:category_slug>/', views.thread_list, name='thread_list'),
    path('<slug:category_slug>/new/', views.create_thread, name='create_thread'),
    path('<slug:category_slug>/<slug:thread_slug>/', views.thread_detail, name='thread_detail'),
]
