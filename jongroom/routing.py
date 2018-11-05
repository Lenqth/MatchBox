from django.urls import path
from .socket_consumer import *
from channels.routing import URLRouter

channel_routing = [
    path("jong/lobby", RoomListConsumer),
    path("jong/room/<str:room_name>", MainConsumer),
    
]
