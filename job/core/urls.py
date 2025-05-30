"""
URL configuration for job project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from job.accounts import views as acc_views  # ✅ full path

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core Pages
    path('', acc_views.home, name='home'),
    path('register/', acc_views.register, name='register'),
    path('accounts/logout/', acc_views.custom_logout, name='logout'),

    # Auth & Social Login
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password reset, etc.
    path('oauth/', include('social_django.urls', namespace='social')),

    # Jobs + User Features
    path('jobs/', include('job.accounts.urls')),  # ✅ full path to app's URLs
]

# Serve media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
