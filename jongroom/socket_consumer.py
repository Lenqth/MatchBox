#
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
import json
from pprint import pprint
from .room import Room
import asyncio

group_cnt = 0

class DelayedEchoConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = asyncio.get_event_loop()

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        self.loop.create_task( self.process_recv(text_data) )

    async def process_recv(self,text_data):
        await asyncio.sleep(5)
        await self.send(text_data=text_data)

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
            await self.reject()
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
            self.room.receive(self,data)
        else:
            message = data['message']
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'chat_message',
                    'message': message })

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def chat_broadcast(self, event):
        obj = event['obj']
        await self.send(text_data=json.dumps(obj))



class JongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        acc = self.accept()
        result = await ( Room.random_match(self) )
        self.room = result["room"]
        self.token = result["token"]
        self.room_pos = result["pos"]
        self.room_name = self.room.name
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await acc
        await self.send(text_data=json.dumps({
            'room' : self.room_name ,
            'token' : self.token ,
            'position' : self.room_pos ,
            'message': "welcome!",
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.room.disconnect(self)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        if self.room is not None :
            self.room.receive(self,data)


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def chat_broadcast(self, event):
        obj = event['obj']
        await self.send(text_data=json.dumps(obj))

    # Receive message from room group
    async def jong_leader(self, event):
        self.leader = event['leader_channel']
