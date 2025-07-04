from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('forum/', include('forum.urls', namespace='forum')),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),
]


urlpatterns += [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # includes login/logout
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
