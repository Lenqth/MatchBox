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
from django.urls import path

from .views import *

urlpatterns = [
    #    path('', WebPackIndex.as_view(), name='home'),
    path('login', LoginAjax.as_view(), name='login_ajax'),
    path('account', GetLoginStateAjax.as_view(), name='account_ajax'),
    path('logout', LogoutAjax.as_view(), name='logout_ajax'),
    path('config/<str:game_type>', Config.as_view(), name='config'),
    #path('', RoomSelect.as_view(), name='home') ,
    #path('room', Room.as_view(), name='room') ,
    #path('jong', Jong.as_view(), name='jong') ,
    #path('quarto', Quarto.as_view(), name='quarto') ,
    #path('testindex', TestIndex.as_view(), name='quarto') ,
]
