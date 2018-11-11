# -*- coding : uft8 -*-

try:
    from .util import *
    from .config import *
except:
    from util import *
    from config import *

import numpy as np
import functools,itertools
import collections

class Yaku:
    def __init__(self,name,cname,score,override=[],bonus=False,multiple=False):
        self.name = name
        self.chinese_name = cname
        self.score = score
        self.override = override
        self.bonus = bonus
        self.multiple = multiple
    def __repr__(self):
        return "( {0} : {1} pts. )".format(self.chinese_name,self.score)
    def toJSON(self):
        return {"name":name,"chinese_name":chinese_name,"score":score}

class ScoreCalculation:
    def __init__(self,checker=None):
        li = list( filter( lambda x: len(x)>0 and x[0]!="_" , dir(checker) ))
        self.yakuchecker = []
        self.yaku=[]
        for x in li:
            q = getattr(checker,x)
            if isinstance(q,Yaku):
                self.yaku.append(q)
            elif hasattr(q,"__yakuroutine__"):
                self.yakuchecker.append(q)


    def calc_score(self,mentu,env={}):
        if isinstance(mentu,list):
            mx = 0
            my = []
            for m in mentu:
                x,y = self.calc_score(m,env=env)
                if mx < x:
                    mx = x
                    my = y
            return (mx,my)

        yaku = []
        for x in self.yakuchecker :
            try:
                res = x(env,mentu)
            except:
                continue
            if res is None:
                continue
            if isinstance(res, collections.Iterable) :
                yaku.extend(res)
            else:
                yaku.append(res)
        total = 0
        res_yaku = []
        for x in yaku:
            total += x.score
        return (total,yaku)


    def add_yaku(self,yaku):
        self.yaku.append(yaku)



def calc_score(mentu,env):
    pass

# CHINESE DEFAULT SET

def safe_get(dic,key,default=None):
    if key in dic  :
        return dic[key]
    else:
        return default

def yakuroutine(x):
    x.__yakuroutine__ = True
    return x

tricolor = list(itertools.permutations([0,1,2]))
class ChineseScore:
    # mentu array format
    #
    # mentu[chow:0,pong:1][color:man,pin,sou,ji][number:1~9]
    #
    @classmethod
    def judge(cls,tiles,mentu,env):
        pass

    @classmethod
    def list_yaku(cls,tiles,mentu,env):
        obj = cls()
        obj.mentu = mentu
        obj.conc_mentu = []
        obj.atama = None
        for m in mentu:
            if m.type == Mentu.ATAMA :
                obj.atama = m.head
        obj.chows = np.zeros( (4,16) , dtype = np.int16 )
        obj.pongs = np.zeros( (4,16) , dtype = np.int16 )
        obj.cpongs = np.zeros( (4,16) , dtype = np.int16 )
        for x in mentu :
            if x.is_concealed():
                conc_mentu.append(mentu)
            if x.is_chow() :
                obj.chows[x.get_color(),x.get_number()] += 1
            if x.is_pongorkong() :
                obj.pongs[x.get_color(),x.get_number()] += 1
                if x.is_concealed():
                    obj.cpongs[x.get_color(),x.get_number()] += 1
        obj.tiles = tiles
        obj.env["flowers"]

    flowerbonus      = Yaku( "Flower" , "花牌" , 1  )

    @yakuroutine
    def flowers(self):
        for i in range(safe_get(self.env,"flowers",0)):
            yield flowerbonus


    machi_tanki   = Yaku( "Single Wait" , "単調将" ,  1  )
    machi_closed  = Yaku( "Closed Wait" , "坎張" ,  1  )
    machi_edge    = Yaku( "Edge Wait" , "辺張" ,  1  )

    pong_t_or_h      = Yaku( "Pong Of Terminals/Honors" , "么九刻" , 1  )

    outside          = Yaku( "Outside Hand" , "全帯么" , 4  )
    all_fives        = Yaku( "All Fives" , "全帯五" , 16  )

    onevoid          = Yaku( "One Voided Suit" , "缺一門" , 1  )
    halfflush        = Yaku( "Half Flush" , "混一色" , 6  )
    fullflush        = Yaku( "Full Flush" , "清一色" , 24  )
    alltypes         = Yaku( "All Types" , "五門斉" , 6  )
    @yakuroutine
    def types(self):
        map(id2suit,self.tiles)

    four             = Yaku( "Tile Hog" , "四帰一" , 2  )

    allevenpong      = Yaku( "All Even Pongs" , "全双刻" ,     24  )

    allchow = Yaku("All Chows","平和",2)

    knit = Yaku( "Lesser Honors And Knitted Tiles" , "全不靠" , 12  )
    knit7 = Yaku( "Greater Honors And Knitted Tiles" , "七星不靠" , 24  )

    ninegates = Yaku( "Nine Gates" , "九蓮宝燈" , 88  )

    @yakuroutine
    def f_nine_gates(self):
        if len(self.conc_mentu)==0 :
            suit = id2suit( self.tiles[0] )
            if np.all( map(id2suit,self.tiles) == suit ):
                 nums = map(id2number,self.tiles)
                 if np.all( nums - [0,3,1,1,1,1,1,1,1,3] >= 0 ):
                     return ninegates

    termchowsp = Yaku( "Pure Terminal Chows" , "一色双龍会" , 64  )
    termchowsm = Yaku( "Three-Suited Terminal Chows" , "三色双龍会" , 16  )
    @yakuroutine
    def termchows(self):
        atama = self.atama
        if not ( id2suit <=2 and id2number(atama) == 5 ) :
            return None
        if np.all( chows[id2suit(atama),[1,9]] == 2 ) :
            return ChineseScore.termchowsp
        for c in range(3):
            if c == id2suit(atama) :
                if np.all( chows[c,[1,9]] == 1 ):
                    pass
                else:
                    return None
        return ChineseScore.termchowsm

    sevenpairs  = Yaku( "Seven Pairs" , "七対" , 24  )
    sevenpairsh = Yaku( "Seven Shifted Pairs" , "連七対" , 88  )



    lasttile = Yaku( "Last Tile" , "和絶張" , 4  )
    lastdraw  = Yaku( "Last Tile Draw" , "妙手回春" , 8  ) #
    lastclaim = Yaku( "Last Tile Claim" , "海底撈月" , 8  ) #
    repltile = Yaku( "Out With Replacement Tile" , "槓上開花" , 8  )#
    robkong = Yaku( "Robbing The Kongs" , "搶槓和" , 8  )

    @yakuroutine
    def state_yaku(self):
        if safe_get(self.env,"lefttile",-1) == 0:
            if safe_get(self.env,"tsumo",False) :
                yield ChineseScore.lastdraw
            else:
                yield ChineseScore.lastclaim
        if "konged_tile" in env and env["konged_tile"] == True :
            yield ChineseScore.repltile
        if "robbed_tile" in env and env["robbed_tile"] == True :
            yield ChineseScore.robkong

    chicken = Yaku( "Chicken Hand" , "無番和" , 8  )



    purest = Yaku("Pure Straight","清龍",16)
    knittedst = Yaku("Knitted Straight","組合龍",12)
    mixedst = Yaku("Mixed Straight","花龍",8)
    @yakuroutine
    def straight(self):
        if mentu["type"] != "normal":
            if mentu["type"] == "knitted_normal":
                return ChineseScore.knittedst
            elif mentu["type"] == "knitted" :
                return ChineseScore.knittedst
            return None
        chows = self.chow
        pure = np.all( chows[:,[1,4,7]]>0 , axis=1).any()
        if pure :
            return ChineseScore.purest
        for r in tricolor:
            if chows[0,1+r[0]*3] > 0 and chows[1,1+r[1]*3] > 0 and chows[2,1+r[2]*3] > 0:
                return ChineseScore.mixedst

    kong4  = Yaku("4 Kongs","四槓",88)#
    kong3  = Yaku("3 Kongs","三槓",32)#
    kong2c = Yaku("2 Concealed Kongs","双暗槓",8)#
    kong2  = Yaku("2 Kongs","双明槓",4)#
    kong1c = Yaku("Concealed Kong","暗槓",2)#
    kong1  = Yaku("Kong","明槓",1)#

    @yakuroutine
    def kongs(self):
        kongs = filter( lambda x:x.is_kong(), self.mentu )
        conckongs = filter( lambda x:x. x.is_concealed(), kongs )
        kl = len(kongs)
        ckl = len(conckongs)
        res = []
        if kl >= 4:
            if ckl >= 2:
                res.append(kong2c)
            elif ckl >= 1:
                res.append(kong1c)
            res.append(kong4)
        elif kl >= 3 :
            if ckl >= 2:
                res.append(kong2c)
            elif ckl >= 1:
                res.append(kong1c)
            res.append(kong3)
        elif kl >= 2 :
            if ckl >= 2:
                res.append(kong2c)
            elif ckl >= 1:
                res.append(kong2)
                res.append(kong1c)
            else:
                res.append(kong2)
        elif kl >= 1 :
            if ckl >= 1:
                res.append(kong1c)
            else:
                res.append(kong1)
        return res

    menzen           = Yaku( "Concealed Hand" , "門前清" ,  2  )
    selfdrawn        = Yaku( "Self Drawn" , "自摸" ,  1  )
    menzentsumo      = Yaku( "Fully Concealed" , "不求人" ,  4  )
    allmeld          = Yaku( "Melded Hand" , "全求人" ,  6  )
    @yakuroutine
    def melds(self):
        meldcnt = len(filter(lambda x:not x.is_concealed() , self.mentu ))
        if safe_get(self.env,"tsumo",False) :
            if meldcnt == 0:
                return menzentsumo
            else:
                return selfdrawn
        else:
            if meldcnt == 4:
                return allmeld
            elif meldcnt == 0:
                return menzen

    allpong = Yaku("All Pongs","碰碰和",6)#
    pong4c = Yaku( "4 Concealed Pongs" , "四暗刻" , 64  )#
    pong3c = Yaku( "3 Concealed Pongs" , "三暗刻" , 16  )#
    pong2c = Yaku( "2 Concealed Pongs" , "双暗刻" , 2  )#

    @yakuroutine
    def pongs(self):
        pongs = self.pongs
        cpongs = self.cpongs
        if not safe_get(self.env,"tsumo",False) :
            a = player.agari_tile
            fq = player.hand_freq_array()
            if fq[a] == 3 and cpongs[a//16,a%16] >= 1 :
                cpongs[a//16][a%16] -= 1
        s = np.sum( cpongs )
        if np.sum(pongs) >= 4 :
            yield ChineseScore.allpong
        if s >= 4:
            return ChineseScore.pong4c
        elif s >= 3 :
            return ChineseScore.pong3c
        elif s >= 2 :
            return ChineseScore.pong2c

    step4p   = Yaku( "Four Shifted Chows" , "一色四歩高" , 32  )#
    step3p   = Yaku( "Three Shifted Chows" , "一色三歩高" , 16  )#
    step3mp  = Yaku( "Mixed Shifted Chows" , "三色三歩高" , 6  )#
    @yakuroutine
    def steps(self):
        chows = self.chows
        for c in range(3):
            for i in range(1,6):
                if chows[c,i] == 0 :
                    continue
                if chows[c,i+1] > 0 and chows[c,i+2] > 0 :
                    if chows[c,i+3]>0 :
                        return ChineseScore.step4p
                    else:
                        return ChineseScore.step3p
                if chows[c,i+2] > 0 and chows[c,i+4] > 0 :
                    if chows[c,i+6]>0 :
                        return ChineseScore.step4p
                    else:
                        return ChineseScore.step3p
        for r in tricolor:
            for i in range(10):
                if chows[0,i+r[0]] > 0 and chows[1,i+r[1]] > 0 and chows[2,i+r[2]] > 0:
                    return ChineseScore.step3mp
        return None

    pong4sh  = Yaku( "Four Pure Shifted Pongs" , "一色四節高" , 48  )#
    pong3sh  = Yaku( "Triple Pure Shifted Pongs" , "一色三節高" , 24  )#
    pong3msh = Yaku( "Mixed Shifted Pongs" , "三色三節高" , 6  )#
    @yakuroutine
    def shifted(self):
        pongs = self.pongs
        for c in range(3):
            for i in range(1,8):
                if pongs[c,i] == 0 :
                    continue
                if pongs[c,i+1] > 0 and pongs[c,i+2] > 0 :
                    if pongs[c,i+3]>0 :
                        return ChineseScore.pong4sh
                    else:
                        return ChineseScore.pong3sh
        for r in tricolor:
            for i in range(9):
                if pongs[0,i+r[0]] > 0 and pongs[1,i+r[1]] > 0 and pongs[2,i+r[2]] > 0:
                    return ChineseScore.pong3msh
        return None




    pong3s = Yaku( "Triple Pong" , "三同刻" , 16  )#
    pong2s = Yaku( "Double Pong" , "双同刻" , 2  )#
    @yakuroutine
    def samepong(self):
        cnt = np.sum( self.pongs > 0 , axis = 0 )
        if ( cnt >= 3 ).any() :
            return ChineseScore.pong3s
        if ( cnt >= 2 ).any() :
            return ChineseScore.pong2s

    chow4s   = Yaku( "Quadruple Chow" , "一色四同順" , 48  )#
    chow3s   = Yaku( "Pure Triple Chow" , "一色三同順" , 24  )#
    chow3ms  = Yaku( "Mixed Triple Chow" , "三色三同順" , 8  )#
    @yakuroutine
    def samechow(self):
        cnt = np.sum( self.chows > 0 , axis = 0 )
        if ( q >= 4 ).any():
            return ChineseScore.chow4s
        if ( q >= 3 ).any():
            return ChineseScore.chow3s
        cnt = np.sum( q > 0 , axis = 0 )
        if ( cnt >= 3 ).any() :
            return ChineseScore.chow3ms

    wind4  = Yaku("Big Four Kongs","大四喜",88)
    wind4s = Yaku("Little Four Kongs","小四喜",64)
    wind3  = Yaku("Three Winds","三風刻",12)
    prev_wind = Yaku( "Prevalent Wind" , "圏風刻" , 2  )
    seat_wind  = Yaku( "Seat Wind" , "門風刻" , 2  )
    dragon3  = Yaku("Big Three Dragons","大三元",88)
    dragon3s = Yaku("Little Three Dragons","小三元",64)
    dragon2  = Yaku("Two Dragons","双箭刻",6)
    dragon1  = Yaku("Dragon Pong","箭刻",2)
    @yakuroutine
    def winds_and_dragons(self):
        chpongs = self.pongs[3]
        pw = safe_get(self.env,"prevalent_wind",-1)
        sw = safe_get(self.env,"seat_wind",-1)
        atama = filter( lambda x:x.type == Mentu.ATAMA , self.mentu )
        if len(atama) > 0:
            atama = atama[0].head
        else:
            atama = -1
        if ( chpongs[0:4] > 0 ).all():
            return ChineseScore.wind4
        if np.sum( chpongs[0:4] > 0 ) >= 3 :
            if 49 <= atama < 49 + 4 :
                yield ChineseScore.wind4s
            else:
                yield ChineseScore.wind3
        dragons = np.sum( chpongs[4:7] > 0 )
        if dragons >= 3 :
            yield ChineseScore.dragon3
        elif dragons >= 2 :
            if 53 <= atama < 53 + 3 :
                yield ChineseScore.dragon3s
            else:
                yield ChineseScore.dragon2
        elif dragons >= 1:
            yield ChineseScore.dragon1

        if chpongs[pw] > 0 :
            yield ChineseScore.prev_wind
        if chpongs[sw] > 0 :
            yield ChineseScore.seat_wind

    chow2m           = Yaku( "Mixed Double Chow" , "喜相逢" , 1  )#
    chow2p           = Yaku( "Pure Double Chow" , "一般高" , 1  )#
    six              = Yaku( "Short Straight" , "連六" , 1  )#
    twoterms         = Yaku( "Two Terminal Chows" , "老少副" , 1  )#
    @yakuroutine
    def twochows(self):
        chows = self.chows
        ipp = np.sum(chows >= 2)
        kso = np.sum( ( np.sum(chows,axis=0) - np.max(chows,axis=0) ) > 0 )
        rsf = np.sum( np.min( chows[ : , [1,7] ] , axis=1 ) > 0 )
        sx = np.sum( np.minimum( chows[:,1:5] , chows[:,4:8] ) > 0 )
        doubled = False
        if ipp > 0:
            yield ChineseScore.chow2p
            if ipp >= 2 and not doubled :
                doubled = True
                yield ChineseScore.chow2p
        if kso > 0:
            yield ChineseScore.chow2m
            if kso >= 2 and not doubled :
                doubled = True
                yield ChineseScore.chow2m
        if rsf > 0:
            yield ChineseScore.twoterms
            if rsf >= 2 and not doubled :
                doubled = True
                yield ChineseScore.twoterms
        if sx > 0:
            yield ChineseScore.six
            if sx >= 2 and not doubled :
                doubled = True
                yield ChineseScore.six

    no_honor         = Yaku( "No Honor" , "無字" , 1  )
    all_simples      = Yaku( "All Simples" , "断么" ,  2  )
    upp4 = Yaku( "Upper Four" , "大于五" ,      12  )
    low4 = Yaku( "Lower Four" , "小于五" ,     12  )
    upp3 = Yaku( "All Upper Tiles" ,  "全大" ,   24  )
    mid3 = Yaku( "All Middle Tiles" ,  "全中" ,  24  )
    low3 = Yaku( "All Lower Tiles" , "全小" , 24 )
    allgreen = Yaku( "All Green" , "緑一色" , 88 )
    allsymm = Yaku( "Reversible Tiles" , "推不倒" , 8 )
    all_t_or_h = Yaku( "All Terminals/Honors" , "混么九" , 32  )
    allhonor = Yaku( "All Honors" , "字一色" ,        64  )
    allterm = Yaku( "All Terminals" , "清么九" ,     64  )
    orphans13 = Yaku( "Thirteen Orphans" , "十三么" , 88  )
    @yakuroutine
    def contain(self):
        tileset = set(self.tiles)
        if tileset.issubset( set( [ 2,3,4,5,6,7,8, 18,19,20,21,22,23,24 , 34,35,36,37,38,39,40 ] ) ) :
            yield all_simples
        elif tileset.issubset( set( [ 1,2,3,4,5,6,7,8,9, 17,18,19,20,21,22,23,24,25 , 33,34,35,36,37,38,39,40,41 ] ) ) :
            yield no_honor


        if tileset.issubset( set( [ 4,5,6, 20,21,22 , 36,37,38 ] ) ) :
            yield mid3

        if tileset.issubset( set( [ 1,2,3, 17,18,19 , 33,34,35 ] ) ) :
            yield low3
        elif tileset.issubset( set( [ 1,2,3,4, 17,18,19,20 , 33,34,35,36 ] ) ) :
            yield low4

        if tileset.issubset( set( [ 7,8,9, 23,24,25 , 39,40,41 ] ) ) :
            yield upp3
        elif tileset.issubset( set( [ 6,7,8,9, 22,23,24,25 , 38,39,40,41 ] ) ) :
            yield upp4

        if tileset.issubset( set( [ 34,35,36,38,40,54 ] ) ) :
            yield allgreen

        if tileset.issubset( set( [ 49,50,51,52,53,54,55 ] ) ) :
            yield allhonor

        if tileset.issubset( set( [ 1,9,16+1,16+9,32+1,32+9 ] ) ) :
            yield allterm

        if tileset.issubset( set( [ 1,9,16+1,16+9,32+1,32+9,49,50,51,52,53,54,55 ] ) ) :
            yield all_t_or_h




#print( list( filter( lambda x: len(x)>0 and x[0]!="_" , dir(ChineseScore) )) )
# sc = ScoreCalculation(checker=ChineseScore)
# print(len( sc.yaku ))
# print( ",".join( map( lambda x: x.chinese_name , sc.yaku ) ) )

"""
            "prevalent_wind": game.prevalent_wind ,
            "seat_wind": game.get_seat_wind(self.id),
            "tsumo":tsumo ,
            "agari_tile":tile,
            "deck_left":game.lefttile(),
            "discarded_tiles": [ self.trash for p in game.players ],
            "exposed_tiles": [ self.exposed for p in game.players ]
"""


if __name__ == "__main__" :
#    unittest.main()
    import unittest
    import agari
    def getmentu(str):
        m = string_to_array(str)
        return agari.is_agari(m)


    class TestScore(unittest.TestCase):
        __sc__ = ScoreCalculation(ChineseScore)
        def test(self):
            pass
    print(TestScore.__sc__.calc_score( getmentu("678m231s345666pSS") ) )
    #print(TestScore.__sc__.calc_score(getmentu("123m234p345sEEESS") ) )
    #print(TestScore.__sc__.calc_score(getmentu("123m456p123789sSS") ) )
    #print(TestScore.__sc__.calc_score(getmentu("123789123789mWW") ) )
    print( string_to_list_ex("67m 123456789s 99p 5m!") )
    print( string_to_list_ex("*456p *789m *567s 5678p 5p") )
    print( string_to_list_ex("*SSS *777s *111m 888s H H!") )
