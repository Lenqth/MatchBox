"""jong_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth.views import login, logout
import django.contrib.auth.views as auth_views

urlpatterns = [
    path('superusers/', admin.site.urls),
    path('api/', include('matchbox.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        extra_context={
            'next': '/jong/',
        }), name='login'),
    path('logout/', logout, name='logout'),
    path('accounts/', include('accounts.urls')),
]
