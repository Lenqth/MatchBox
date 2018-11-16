# -*- coding : uft8 -*-

from util import *

class Mentu:
    CHOW = 1
    PUNG = 2
    MINKONG = 3
    APKONG = 4
    CONCKONG = 5
    CONCCHOW = 6
    CONCPUNG = 7
    ATAMA = 8
    __TYPENAMES__ = ["","chow","pong","minkong","conckong","apkong","concchow","concpung","atama"]

    def __init__(self,type,head,agari_tile=None):
        self.type = type
        self.head = head
        self.agari_tile = agari_tile

    def __repr__(self):
        if self.type == self.__class__.CHOW :
            return "CHOW( %d,%d,%d )" % (self.head,self.head+1,self.head+2)
        elif self.type == self.__class__.PUNG :
            return "PUNG( %d,%d,%d )" % (self.head,self.head,self.head)
        elif self.type == self.__class__.MINKONG :
            return "MINKONG( %d,%d,%d,%d )" % (self.head,self.head,self.head)
        elif self.type == self.__class__.APKONG :
            return "APKONG( %d,%d,%d,%d )" % (self.head,self.head,self.head,self.head)
        elif self.type == self.__class__.CONCKONG :
            return "CONCKONG( %d,%d,%d,%d )" % (self.head,self.head,self.head,self.head)
        elif self.type == self.__class__.CONCCHOW :
            return "CONCCHOW( %d,%d,%d,%d )" % (self.head,self.head+1,self.head+2)
        elif self.type == self.__class__.CONCPUNG :
            return "CONCPUNG( %d,%d,%d,%d )" % (self.head,self.head,self.head)
        elif self.type == self.__class__.ATAMA :
            return "ATAMA( %d,%d )" % (self.head,self.head)

    def get_tiles(self):
        if self.type == self.__class__.CHOW or self.type == self.__class__.CONCCHOW :
            return (self.head,self.head+1,self.head+2)
        elif self.type == self.__class__.PUNG or self.type == self.__class__.CONCPUNG :
            return (self.head,self.head,self.head)
        elif self.type == self.__class__.MINKONG or self.type == self.__class__.APKONG or self.type == self.__class__.CONCKONG :
            return (self.head,self.head,self.head,self.head)
        elif self.type == self.__class__.ATAMA :
            return (self.head,self.head,self.head,self.head)

    def contains(self,x):
        if self.type == self.__class__.CHOW or self.type == self.__class__.CONCCHOW :
            return self.head <= x <= self.head+2
        else:
            return x == self.head

    def machi(self): # machi type for 1 pts hands
        if self.agari_tile is None :
            return None
        if self.type == self.__class__.CONCCHOW :
            if self.agari_tile == self.head + 1 :
                return "KANCHAN"
            elif self.agari_tile == self.head and id2number(self.head) == 7 :
                return "PENCHAN"
            elif self.agari_tile == self.head + 2 and id2number(self.head) == 1 :
                return "PENCHAN"
            else:
                return "OTHER"
        elif self.type == self.__class__.ATAMA :
            return "TANKI"
        else:
            return "OTHER"

    @classmethod
    def from_mentu_array(cls,data,atama=None):
        nzs = data.nonzero()
        res = []
        if atama is not None:
            res.append( cls( cls.ATAMA , atama ) )
        types , suits , nums = nzs
        for j in range(len(nums)) :
            type , suit , num = types[j] , suits[j] , nums[j]
            for i in range( data[type,suit,num] ):
                res.append( cls( 7 - type  , suit * 16 + num ) )
        return res


    def toDict(self):
        return {"type":self.__class__.__TYPENAMES__[self.type] , "tiles":self.get_tiles() }

    def mentu_id(self):
        return self.head

    def is_kong(self):
        return self.type >= self.__class__.MINKONG or self.type == self.__class__.CONCKONG or self.type == self.__class__.APKONG

    def is_pong(self):
        return self.type >= self.__class__.PUNG or self.type == self.__class__.CONCPUNG

    def is_chow(self):
        return self.type >= self.__class__.CHOW or self.type == self.__class__.CONCCHOW

    def is_pongorkong(self):
        return self.is_pong() or self.is_kong()

    def is_conc_pongorkong(self):
        return ( self.is_pong() or self.is_kong() ) and self.is_concealed()

    def is_concealed(self):
        return self.type == self.__class__.CONCKONG or self.type == self.__class__.CONCCHOW or self.type == self.__class__.CONCPUNG

    def get_color(self):
        return self.head // 16

    def get_number(self):
        return self.head % 16

    def toJSON(self):
        return self.toDict()
