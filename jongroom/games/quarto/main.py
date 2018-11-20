
async def main(players,settings={}):
    pass

def Agent:
    def select(self):
        pass

    def turn(self):
        pass

def AgentPlayer(Agent):
    def select(self):
        pass

    def turn(self):
        pass


def Quarto:
    async def start():
        board = np.zeros( (4,4) ,dtype=np.int32 )
        piecevalue = []
        pieceleft = np.ones( (16,) ,dtype=np.int16 )
        for i in range(16):
            piece.append( (i << 4) | (~i) )
