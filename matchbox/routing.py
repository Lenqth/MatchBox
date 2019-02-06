from django.urls import path
from .socket_consumer import *
from channels.routing import URLRouter

channel_routing = [
    path("ws/jong/lobby", RoomListConsumer),
    path("ws/jong/room/auto", MainConsumer),
    path("ws/jong/room/configured", ConfiguredMainConsumer),
    path("ws/jong/room/join/<str:room_id>", MainConsumer),
]
