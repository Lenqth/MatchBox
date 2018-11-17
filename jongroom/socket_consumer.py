#
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
import json
from pprint import pprint
from .room import Room
import asyncio

group_cnt = 0

class RoomListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            "lobby_listener",
            self.channel_name
        )
        await self.receive("")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "lobby_listener",
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = {}
        try:
            data = json.loads(text_data)
        except:
            pass
        rooms = []
        for (k,v) in Room.rooms.items():
            rooms.append( {"room_id":k,"room_pop":v.room_population , "room_cap":v.room_size , "state":v.room_state } )
        await self.send(text_data=json.dumps({
            'rooms' : rooms ,
        }))

    async def lobby_refresh(self, event):
        await self.receive("")

class MainConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.onreceive = []
        token = None
        if str(self.scope["user"]) != "" :
            token = str( self.scope["user"] )
        elif "token" in self.scope["session"] :
            token = self.scope["session"]["token"]
        await self.accept()
        result = await ( Room.random_match(self,None) )
        if result == None:
            return
        # Join room group
        self.scope["session"]["token"] = self.token
        self.loop = asyncio.get_event_loop()

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self,"room"):
            await self.room.disconnect(self)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        self.loop.create_task( self.receive_async(text_data) )


    # Receive message from WebSocket
    async def receive_async(self, text_data):
        data = json.loads(text_data)
        #print(data)
        for handler in self.onreceive:
            handler(data)

        if self.room is not None :
            await self.room.receive(self,data)
        else:
            print("no room")

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def chat_broadcast(self, event):
        obj = event['obj']
        print(obj)
        await self.send(text_data=json.dumps(obj))
