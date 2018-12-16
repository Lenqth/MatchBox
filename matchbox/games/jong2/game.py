
from games.common.store import *


class AgentAI:
    pass

class Manipulator:
    
    def __init__(self,store):
        self.store = store

    def reset(self):
        self.store["deck"] = []
        pass

    def discard(self,pos):
        pass
    
    def draw(self,pl):
        tile = self.store["deck"].pop(-1)
        self.store["players"][pl]["hand"].append()

    def claim(self,pl,cmd):
        pass

    @property
    def command_list(self,pl):
        pass

    @property
    def claim_command_list(self,pl):
        pass


class Game:

    def __init__(self):
        self.store = to_observable({})
        self.manipulator = Manipulator(self.store)

    def main(self):
        pass