# -*- coding : uft8 -*-


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
    def __init__(self,type,head):
        self.type = type
        self.head = head

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
