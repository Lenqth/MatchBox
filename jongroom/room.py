#
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
import json
from pprint import pprint

from .python_jong.game import *
from .python_jong.player import *
from .python_jong.agent import *

from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

import secrets,traceback
import time
class RoomException(Exception):
    pass

class Room:

    rooms = {}

    @classmethod
    async def random_match(cls,channel,token=None):
        room_id = None
        res = None
        if token != None :
            try:
                room_id = token[0:32]
                res = await cls.rooms[room_id].connect(channel,token)
            except RoomException as e:
                pass
            return res
        for room in cls.rooms.values():
            try:
                res = await room.connect(channel,token)
            except RoomException as e:
                pass
            return res
        room = cls()
        await room.on_room_created(room.name)
        print("room created [{0}]".format(room.name))
        cls.rooms[room.name] = room
        res = await room.connect(channel)
        return res


    @property
    def room_size(self):
        return 1

    @property
    def room_population(self):
        res = 0
        for (i,v) in enumerate( self.player_token ) :
            if v is not None :
                res += 1
        return res

    @property
    def room_state(self):
        if self.finalized :
            return "対戦中"
        else:
            return "募集中"

    def __init__(self):
        roomsize = self.room_size
        self.name = secrets.token_hex(16)
        self.player_connection = [None] * roomsize
        self.player_token = [None] * roomsize
        self.finalized = False

    def getplayers(self):
        res = []
        for (i,v) in enumerate( self.player_token ) :
            if v is not None :
                res.append( [i,v] )
        return res


    async def start(self):
        self.finalized = True
        game = Game()
        conns = list( map( GameConnection , self.player_connection ) )
        self.conns = conns
        for i in range(4):
            game.players[i].agent = AITsumogiri()
        game.players[0].agent = RemotePlayer( conns[0] )
        try:
            await game.one_game()
        except Exception as e :
            traceback.print_exc()
        await self.destroy_room()

    async def destroy_room(self):
        roomname = self.name
        del self.__class__.rooms[self.name]
        await self.on_room_destroyed(roomname)
        print("room destroyed [{0}]".format(roomname))

    def receive(self,channel,data):
        pos = channel.room_pos
        try:
            #if data["type"] == "get_all" :
            #    pass
            pass
        except:
            return {"error":""}


    async def on_room_created(self,room_id):
        await channel_layer.group_send(
            "lobby_listener",
            {
                'type': 'lobby_refresh',
                'obj' : {}
            }
        )

    async def on_room_destroyed(self,room_id):
        await channel_layer.group_send(
            "lobby_listener",
            {
                'type': 'lobby_refresh',
                'obj' : {}
            }
        )

    async def on_room_join(self,joined_player,position):
        await channel_layer.group_send(
            'chat_%s' % self.name,
            {
                'type': 'chat_broadcast',
                'obj' : {"joined": [ position ,  joined_player] , "message":"joined:{0}".format(joined_player)}
            }
        )

    async def on_room_exit(self,player,position):
        await channel_layer.group_send(
            'chat_%s' % self.name,
            {
                'type': 'chat_broadcast',
                'obj' : {"exited": [ position , player] , "message":"exited:{0}".format(player)}
            }
        )

    async def connect(self,channel,token=None):
        if token is not None :
            try:
                res = await self.reconnect(channel,token)
                return ress
            except RoomException as e:
                pass
        i = 0
        while i < self.room_size and self.player_connection[i] != None :
            i+=1
        if i >= self.room_size :
            raise RoomException("room capacity over")
        token = self.name + secrets.token_hex(16)
        self.player_connection[i] = channel
        self.player_token[i] = token
        await self.on_room_join(token,i)
        return {"room":self,"token":token,"pos":i}

    async def disconnect(self,channel):
        nones = 0
        for (i,x) in enumerate( self.player_connection ) :
            if x == channel :
                self.player_connection[i] = None
                if not self.finalized :
                    await self.on_room_exit(self.player_token[i],i)
                    self.player_token[i] = None
                nones += 1
            elif x is None:
                nones += 1
        if nones == self.room_size:
            await self.destroy_room()


    async def reconnect(self,channel,token):
        for i in range(4):
            if self.player_token[i] == token :
                self.player_connection[i] = channel
                return {"room":self,"token":token,"pos":i}
        raise RoomException("token doesn't match")


    def listener(self,obj):
        pass

class myJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, map):
            return list(obj)
        elif hasattr(obj,"toJSON"):
            return obj.toJSON()
        else:
            print("JSON : {0}".format(type(obj)))
            return super(myJSONEncoder, self).default(obj)

class SkipHandler(Exception):
    pass

class GameConnection:

    def __init__(self,conn):
        self.__receive_handlers = set()
        self._m_id = 0
        self.conn = conn
        self.wait_for_reply = {}
        conn.onreceive.append(self.push_received)

    def replace_connection(self,conn):
        self.conn = conn
        print("connection replaced")


    def push_received(self,obj):
        rem = []
        for f in self.__receive_handlers:
            try:
                res = f(obj)
                if res == True :
                    rem.append(f)
                    break
            except SkipHandler:
                pass
        for x in rem:
            self.remove_receive_handler(x)

    async def send(self,obj):
        txt = json.dumps(obj,cls = myJSONEncoder)
        await self.conn.send(text_data=txt)
        print("{0}".format(txt))

    def add_receive_handler(self,f):
        self.__receive_handlers.add(f)

    def remove_receive_handler(self,f):
        self.__receive_handlers.remove(f)

    async def send_and_receive_reply(self,obj,timeout=30):
        sobj = json.loads( json.dumps(obj , cls = myJSONEncoder ) )
        self._m_id += 1
        sobj["_m_id"] = self._m_id
        m_id = sobj["_m_id"]
        __handler_v = None
        def __promf(res,rej):
            nonlocal __handler_v
            def __handler(obj):
                if "_m_id" in obj and obj["_m_id"] == m_id :
                    res(obj) # delete handler
                    return True
                else:
                    raise SkipHandler("")
            __handler_v = __handler
            self.add_receive_handler(__handler)
        t = Promise( __promf )
        sobj["timeout"] = time.time() + timeout
        await self.send(sobj)
        self.wait_for_reply[ m_id ] = sobj
        try:
            res = await asyncio.wait_for(t,timeout=timeout)
        except Exception as e:
            print("timeout")
            self.remove_receive_handler(__handler_v)
            raise e
            #await self.send( { "timeout":m_id } )
        finally:
            del self.wait_for_reply[ m_id ]
        return res
