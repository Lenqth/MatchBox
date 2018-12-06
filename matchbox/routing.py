from django.urls import path
from .socket_consumer import *
from channels.routing import URLRouter

channel_routing = [
    path("jong/lobby", RoomListConsumer),
    path("jong/room/auto", MainConsumer),
    path("jong/room/configured", ConfiguredMainConsumer),
    path("jong/room/join/<str:room_id>", MainConsumer),

]
