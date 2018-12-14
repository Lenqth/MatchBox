
from games.common.store import *


class AgentAI:
    pass

class Mutator:
    
    def __init__(self,store):
        self.store = store

    def discard(self,pos):
        pass
    

class Action:

    def main(self):
        pass

    



class Game:

    def __init__(self):
        self.store = to_observable({})
        self.mutator = Mutator(self.store)

