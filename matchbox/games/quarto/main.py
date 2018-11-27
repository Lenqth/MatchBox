

import asyncio
from promise import Promise
import traceback

async def main(players,settings={}):
    pass

class Agent:
    def select(self):
        pass

    def turn(self):
        pass

def AgentPlayer(Agent):
    def select(self):
        pass

    def turn(self):
        pass


class Quarto:
    async def start():
        board = np.zeros( (4,4) ,dtype=np.int32 )
        piecevalue = []
        pieceleft = np.ones( (16,) ,dtype=np.int16 )
        for i in range(16):
            piece.append( (i << 4) | (~i) )

async def main(conns,room):
    game = Game(room.config)
    for i in range(4):
        game.players[i].agent = AITsumogiri()
    game.players[0].agent = RemotePlayer( conns[0] )
    if len(conns) >= 2:
        game.players[2].agent = RemotePlayer( conns[1] )
    tasks = [ c.receive_any(timeout=60) for c in conns ]
    tasks2 = [ c.send( { "start" : "1" } ) for c in conns ]
    await Promise.all(tasks2)
    await Promise.all(tasks)
    try:
        await game.run()
    except Exception as e :
        traceback.print_exc()
        raise e


def config():
    obj = {}
    obj["room_size"] = { "display_name":"人数" , "default":2 , "value":[2]  }
    obj["timeout"] = { "display_name":"制限時間" , "default":30 , "value":[15,30,60,300]  }

    return obj
