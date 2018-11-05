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
        token = None
        if "token" in self.scope["session"] :
            token = self.scope["session"]["token"]
        result = await ( Room.random_match(self,token) )
        if result == None:
            return
        acc = self.accept()
        self.room = result["room"]
        self.token = result["token"]
        self.room_pos = result["pos"]
        self.room_name = self.room.name
        self.room_group_name = 'chat_%s' % self.room_name

        self.onreceive = []

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await acc
        self.scope["session"]["token"] = result["token"]
        await self.send(text_data=json.dumps({
            'room' : self.room_name ,
            'token' : self.token ,
            'position' : self.room_pos ,
            'room':self.room.getplayers() ,
            'message': "welcome!",
        }))
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
        print(data)
        for handler in self.onreceive:
            print("handler")
            handler(data)
        if "start" in data :
            print("start")
            await self.room.start()
        elif self.room is not None :
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
