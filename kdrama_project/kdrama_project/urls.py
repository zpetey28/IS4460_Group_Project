"""
URL configuration for kdrama_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

# MovieApp/urls.py
from django.urls import path, include, re_path
from django.contrib import admin
from .views import RegisterView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kdrama/', include('kdrama.urls')),
    path('accounts/',include('django.contrib.auth.urls')),

    path('accounts/register/', RegisterView.as_view(), name='account-register'),
    re_path(r'^$', RedirectView.as_view(url='/accounts/login/', permanent=False)),
]