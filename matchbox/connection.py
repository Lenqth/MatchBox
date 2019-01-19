
import traceback
import secrets
from promise import Promise
import numpy as np
import asyncio
import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
import json
from pprint import pprint

from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


class myJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.bool) or isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, map):
            return list(obj)
        elif hasattr(obj, "toJSON"):
            return obj.toJSON()
        else:
            print("JSON : {0}".format(type(obj)))
            return super(myJSONEncoder, self).default(obj)


class SkipHandler(Exception):
    pass


class GameConnection:

    def __init__(self, conn):
        self.__receive_handlers = set()
        self._m_id = 0
        self.conn = conn
        self.wait_for_reply = {}
        conn.onreceive.append(self.push_received)

    def get_user(self):
        return self.conn.user

    def replace_connection(self, conn):
        self.conn = conn
        print("connection replaced")
        # resend
        for x in self.wait_for_reply:
            pass

    def push_received(self, obj):
        rem = []
        for f in self.__receive_handlers:
            try:
                res = f(obj)
                if res == True:
                    rem.append(f)
            except SkipHandler:
                pass

    async def send(self, obj):
        txt = json.dumps(obj, cls=myJSONEncoder)
        await self.conn.send(text_data=txt)
        print("send : {0}".format(txt))

    def add_receive_handler(self, f):
        self.__receive_handlers.add(f)

    def remove_receive_handler(self, f):
        self.__receive_handlers.remove(f)

    async def receive_any(self, timeout=30):
        __handler_v = None

        def __promf(res, rej):
            nonlocal __handler_v

            def __handler(obj):
                res(obj)
                return True
            __handler_v = __handler
            self.add_receive_handler(__handler)
        t = Promise(__promf)
        # self.wait_for_reply[ m_id ] = sobj
        try:
            res = await asyncio.wait_for(t, timeout=timeout)
        except Exception as e:
            raise e
            # await self.send( { "timeout":m_id } )
        finally:
            self.remove_receive_handler(__handler_v)
            pass
#            del self.wait_for_reply[ m_id ]
        return res

    async def send_and_receive_reply(self, obj, timeout=30):
        sobj = json.loads(json.dumps(obj, cls=myJSONEncoder))
        self._m_id += 1
        sobj["_m_id"] = self._m_id
        m_id = sobj["_m_id"]
        __handler_v = None

        def __promf(res, rej):
            nonlocal __handler_v

            def __handler(obj):
                if "_m_id" in obj and obj["_m_id"] == m_id:
                    res(obj)  # delete handler
                    return True
                else:
                    raise SkipHandler("")
            __handler_v = __handler
            self.add_receive_handler(__handler)
        t = Promise(__promf)
        sobj["timeout"] = time.time() + timeout
        await self.send(sobj)
        self.wait_for_reply[m_id] = sobj
        try:
            res = await asyncio.wait_for(t, timeout=timeout)
        except Exception as e:
            raise e
            # await self.send( { "timeout":m_id } )
        finally:
            self.remove_receive_handler(__handler_v)
            del self.wait_for_reply[m_id]
        return res
