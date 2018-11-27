#
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
import json
from pprint import pprint


from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

import secrets,traceback
import time

from promise import Promise
from .connection import GameConnection

import sys,os

def import_game(game):
    import importlib
    import os,sys
    from .installed_games import INSTALLED_GAMES
    if game in INSTALLED_GAMES :
        try:
            return importlib.import_module( ( ".games.%s.main" % game ) , package=__package__ )
        except:
            return importlib.import_module( ( "games.%s.main" % game ) , package=__package__ )

def default_config(game):
    config = import_game(game).config()

    res = { "game_type": game }
    for (k,v) in config.items():
        res[k] = v["default"]
    return res

class RoomException(Exception):
    pass

class Room:

    rooms = {}

    token_to_room_id = {}

    @classmethod
    async def random_match(cls,channel,token=None):
        room_id = None
        res = None
        if token != None :
            try:
                room_id = token_to_room_id[token]
                res = await cls.rooms[room_id].connect(channel,token)
            except RoomException as e:
                pass
            else:
                return res
        for room in cls.rooms.values():
            try:
                res = await room.connect(channel,token)
            except RoomException as e:
                continue
            else:
                return res
        room = cls()
        await room.on_room_created(room.name)
        print("room created [{0}]".format(room.name))
        cls.rooms[room.name] = room
        res = await room.connect(channel)
        return res

    @classmethod
    async def new_room(cls,config,channel):
        room = cls(config=config)
        await room.on_room_created(room.name)
        print("room created [{0}]".format(room.name))
        cls.rooms[room.name] = room
        res = await room.connect(channel)
        return res


    @property
    def room_size(self):
        return self.config["room_size"]

    @property
    def room_population(self):
        res = 0
        for (i,pl) in enumerate( self.players ) :
            if pl["token"] is not None :
                res += 1
        return res

    @property
    def room_state(self):
        if self.finalized :
            return "対戦中"
        else:
            return "募集中"

    def __init__(self,config=None):
        self.name = secrets.token_hex(16)
        if config == None :
            config = default_config("jong")

        self.config = config
        roomsize = 4
        if "room_size" in config :
            roomsize = self.room_size
        self.players = [ {"token":None , "connection" : None , "ready" : False } for i in range(roomsize) ]
        self.finalized = False

    def getplayers(self):
        res = []
        for (i,pl) in enumerate( self.players ) :
            if pl["token"] is not None :
                res.append( {"position":i,"token":pl["token"],"ready":pl["ready"]} )
        return res


    async def start(self):
        import importlib
        import os,sys
        from .installed_games import INSTALLED_GAMES

        self.finalized = True
        active_users = list( filter( lambda x : x is not None , [ pl["connection"] for pl in self.players ]  ) )
        conns = list( map( lambda conn : GameConnection(conn) , active_users ) )
        self.conns = conns

        game = self.config["game_type"]        
        try:
            await import_game(game).main(conns,self)
        except:
            pass
        await self.destroy_room()

    async def destroy_room(self):
        roomname = self.name
        del self.__class__.rooms[self.name]
        await self.on_room_destroyed(roomname)
        print("room destroyed [{0}]".format(roomname))

    def get_pos_from_token(self,token):
        for (i,pl) in enumerate(self.players):
            if pl["token"] == token:
                return i
        return None

    def all_players_ready(self):
        for (i,pl) in enumerate(self.players):
            if not pl["ready"] :
                return False
        return True

    async def receive(self,channel,data):
        pos = channel.room_pos
        try:
            if "message" in data :
                message = data['message']
                print("@%s" % message )
                await self.room_broadcast( { "from":str(channel.scope["user"]) ,"message" : message } )
            if "ready" in data :
                pos = self.get_pos_from_token(channel.token)
                ready = data["ready"]
                self.players[pos]["ready"] = ready
                await self.room_broadcast( { "set_state":{ "pos" : pos , "ready" : ready  } } )
                if self.all_players_ready():
                    await self.start()
                    pass #スタート

        except Exception as e:
            traceback.print_exc()
            raise e

    async def lobby_broadcast(self,obj):
        await channel_layer.group_send(
            "lobby_listener",
            {
                'type': 'lobby_refresh',
                'obj' : obj
            })

    async def on_room_created(self,room_id):
        await self.lobby_broadcast({})

    async def on_room_destroyed(self,room_id):
        await self.lobby_broadcast({})

    async def room_broadcast(self,obj):
        await channel_layer.group_send(
            'chat_%s' % self.name,
            {
                'type': 'chat_broadcast',
                'obj' : obj
            })

    async def on_room_join(self,joined_player,position):
        await self.room_broadcast( {"joined": {"position":position,"name":joined_player,"ready":False} , "message":"joined:{0}".format(joined_player)} )

    async def on_room_exit(self,player,position):
        await self.room_broadcast( {"exited": {"position":position,"name":player} , "message":"exited:{0}".format(player)} )


    # connect to room
    async def connect(self,channel,token=None):
        if token is not None :
            try:
                res = await self.reconnect(channel,token)
                return ress
            except RoomException as e:
                pass
        i = 0
        while i < self.room_size and self.players[i]["connection"] != None :
            i+=1
        if i >= self.room_size :
            raise RoomException("room capacity over")
        token = self.name + secrets.token_hex(16)
        self.players[i]["connection"] = channel
        self.players[i]["token"] = token
        channel.room = self
        channel.token = token
        channel.room_pos = i
        channel.room_name = self.name
        channel.room_group_name = 'chat_%s' % self.name
        await channel.channel_layer.group_add(
            channel.room_group_name,
            channel.channel_name
        )
        await self.on_room_join(token,i)
        await channel.send(text_data=json.dumps({
            'roomname' : self.name ,
            'token' : token ,
            'position' : i ,
            'roomsize' : self.room_size ,
            'room':self.getplayers() ,
            'message': "welcome!",
        }))
        return True
        # return {"room":self,"token":token,"pos":i,"roomsize":self.room_size,"message":"welcome!"}

    async def disconnect(self,channel):
        nones = 0
        for (i,pl) in enumerate( self.players ) :
            conn = pl["connection"]
            if conn == channel :
                self.players[i]["connection"] = None
                self.players[i]["ready"] = False
                if not self.finalized :
                    await self.on_room_exit(self.players[i]["token"],i)
                    self.players[i]["token"] = None
                nones += 1
            elif conn is None:
                nones += 1
        if nones == self.room_size:
            await self.destroy_room()


    async def reconnect(self,channel,token):
        for i in range(4):
            if self.players[i]["token"] == token :
                self.players[i]["connection"] = channel
                return {"room":self,"token":token,"pos":i,"roomsize":self.room_size}
        raise RoomException("token doesn't match")


    def listener(self,obj):
        pass
