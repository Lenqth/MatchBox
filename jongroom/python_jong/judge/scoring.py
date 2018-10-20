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

class ScoreCalculation:
    def __init__(self,checker=None):
        li = list( filter( lambda x: len(x)>0 and x[0]!="_" , dir(checker) ))
        self.yakuchecker = []
        self.yaku=[]
        for x in li:
            q = getattr(checker,x)
            if isinstance(q,Yaku):
                self.yaku.append(q)
            else:
                self.yakuchecker.append(q)


    def calc_score(self,player,mentu):
        if isinstance(mentu,collections.Iterable):
            mx = 0
            my = []
            for m in mentu:
                x,y = self.calc_score(player,m)
                if mx < x:
                    mx = x
                    my = y
            return (mx,my)

        yaku = []
        for x in self.yakuchecker :
            res = x(player,mentu)
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



def calc_score(player,mentu):
    pass

# CHINESE DEFAULT SET

tricolor = list(itertools.permutations([0,1,2]))
class ChineseScore:
    flowerbonus      = Yaku( "Flower" , "花牌" , 1  )

    machi_tanki   = Yaku( "Single Wait" , "単調将" ,  1  )
    machi_closed  = Yaku( "Closed Wait" , "坎張" ,  1  )
    machi_edge    = Yaku( "Edge Wait" , "辺張" ,  1  )

    pung_t_or_h      = Yaku( "Pung Of Terminals/Honors" , "么九刻" , 1  )

    no_honor         = Yaku( "No Honor" , "無字" , 1  )
    all_simples      = Yaku( "All Simples" , "断么" ,  2  )

    menzen           = Yaku( "Concealed Hand" , "門前清" ,  2  )
    selfdrawn        = Yaku( "Self Drawn" , "自摸" ,  1  )
    menzentsumo      = Yaku( "Fully Concealed" , "不求人" ,  4  )
    allmeld          = Yaku( "Melded Hand" , "全求人" ,  6  )
    four             = Yaku( "Tile Hog" , "四帰一" , 2  )
    outside          = Yaku( "Outside Hand" , "全帯么" , 4  )
    all_fives        = Yaku( "All Fives" , "全帯五" , 16  )
    onevoid          = Yaku( "One Voided Suit" , "缺一門" , 1  )
    halfflush        = Yaku( "Half Flush" , "混一色" , 6  )
    fullflush        = Yaku( "Full Flush" , "清一色" , 24  )
    alltypes         = Yaku( "All Types" , "五門斉" , 6  )
    lasttile         = Yaku( "Last Tile" , "和絶張" , 4  )

    chow2m           = Yaku( "Mixed Double Chow" , "喜相逢" , 1  )#
    chow2p           = Yaku( "Pure Double Chow" , "一般高" , 1  )#
    six              = Yaku( "Short Straight" , "連六" , 1  )#
    twoterms         = Yaku( "Two Terminal Chows" , "老少副" , 1  )#

    allevenpung      = Yaku( "All Even Pungs" , "全双刻" ,     24  )

    allchow = Yaku("Four Kongs","平和",2)
    allpung = Yaku("Four Kongs","碰碰和",6)#

    kong4  = Yaku("4 Kongs","四槓",88)#
    kong3  = Yaku("3 Kongs","三槓",32)#
    kong2c = Yaku("2 Concealed Kongs","双暗槓",8)#
    kong2  = Yaku("2 Kongs","双明槓",4)#
    kong1c = Yaku("Concealed Kong","暗槓",2)#
    kong1  = Yaku("Kong","明槓",1)#


    pong4c = Yaku( "4 Concealed Pungs" , "四暗刻" , 64  )#
    pong3c = Yaku( "3 Concealed Pungs" , "三暗刻" , 16  )#
    pong2c = Yaku( "2 Concealed Pungs" , "双暗刻" , 2  )#

    dragon3  = Yaku("Big Three Dragons","大三元",88)
    dragon3s = Yaku("Little Three Dragons","小三元",64)
    dragon2  = Yaku("Two Dragons","双箭刻",6)
    dragon1  = Yaku("Dragon Pung","箭刻",2)

    wind4  = Yaku("Big Four Kongs","大四喜",88)
    wind4s = Yaku("Little Four Kongs","小四喜",64)
    wind3  = Yaku("Three Winds","三風刻",12)
    fieldwind = Yaku( "Prevalent Wind" , "圏風刻" , 2  )
    selfwind  = Yaku( "Seat Wind" , "門風刻" , 2  )

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


    purest = Yaku("Pure Straight","清龍",16)
    knittedst = Yaku("Knitted Straight","組合龍",12)
    mixedst = Yaku("Mixed Straight","花龍",8)

    knit = Yaku( "Lesser Honors And Knitted Tiles" , "全不靠" , 12  )
    knit7 = Yaku( "Greater Honors And Knitted Tiles" , "七星不靠" , 24  )

    chow4s   = Yaku( "Quadruple Chow" , "一色四同順" , 48  )#
    chow3s   = Yaku( "Pure Triple Chow" , "一色三同順" , 24  )#
    chow3ms  = Yaku( "Mixed Triple Chow" , "三色三同順" , 8  )#

    pong3s = Yaku( "Triple Pung" , "三同刻" , 16  )#
    pong2s = Yaku( "Double Pung" , "双同刻" , 2  )#

    pong4sh  = Yaku( "Four Pure Shifted Pungs" , "一色四節高" , 48  )#
    pong3sh  = Yaku( "Triple Pure Shifted Pungs" , "一色三節高" , 24  )#
    pong3msh = Yaku( "Mixed Shifted Pungs" , "三色三節高" , 6  )#

    step4p   = Yaku( "Four Shifted Chows" , "一色四歩高" , 32  )#
    step3p   = Yaku( "Three Shifted Chows" , "一色三歩高" , 16  )#
    step3mp  = Yaku( "Mixed Shifted Chows" , "三色三歩高" , 6  )#

    termchowsp = Yaku( "Pure Terminal Chows" , "一色双龍会" , 64  )
    termchowsm = Yaku( "Three-Suited Terminal Chows" , "三色双龍会" , 16  )

    sevenpairs  = Yaku( "Seven Pairs" , "七対" , 24  )
    sevenpairsh = Yaku( "Seven Shifted Pairs" , "連七対" , 88  )

    lastdraw  = Yaku( "Last Tile Draw" , "妙手回春" , 8  ) #
    lastclaim = Yaku( "Last Tile Claim" , "海底撈月" , 8  ) #
    repltile = Yaku( "Out With Replacement Tile" , "槓上開花" , 8  )#
    robkong = Yaku( "Robbing The Kongs" , "搶槓和" , 8  )

    chicken = Yaku( "Chicken Hand" , "無番和" , 8  )

    ninegates = Yaku( "Nine Gates" , "九蓮宝燈" , 88  )

    # mentu array format
    #
    # mentu[chow:0,pong:1][color:man,pin,sou,ji][number:1~9]
    #
    @staticmethod
    def state_yaku(player,mentu):
        if player == None :
            return None
        game = player.game
        if game.lefttile() == 0:
            if player.is_tsumo() :
                yield lastdraw
            else:
                yield lastclaim
        if game.konged_tile :
            yield repltile


    def straight(player,mentu):
        if mentu["type"] != "normal":
            if mentu["type"] == "knitted_normal" or mentu["type"] == "knitted":
                return ChineseScore.knittedst
            return None
        chows = mentu["data"][1]
        pure = np.all( chows[:,[1,4,7]]>0 , axis=1).any()
        if pure :
            return ChineseScore.purest
        for r in tricolor:
            if chows[0,1+r[0]*3] > 0 and chows[1,1+r[1]*3] > 0 and chows[2,1+r[2]*3] > 0:
                return ChineseScore.mixedst



    @staticmethod
    def kongs(player,mentu):
        if mentu["type"] != "normal":
            return None
        if player == None :
            return None
        kongs = filter( lambda x:x.is_kong(), player.exposed )
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

    @staticmethod
    def melds(player,mentu):
        if mentu["type"] != "normal":
            return None
        if player == None :
            return None
        meldcnt = len(filter(lambda x:not x.is_concealed() , player.exposed))
        if player.is_tsumo() :
            if meldcnt == 0:
                return menzentsumo
            else:
                return selfdrawn
        else:
            if meldcnt == 4:
                return allmeld
            elif meldcnt == 0:
                return menzen

    @staticmethod
    def pungs(player,mentu):
        if mentu["type"] != "normal":
            return None
        if player == None :
            return None
        pungs = mentu["data"][0]
        cpungs = mentu["data"][0].copy()
        for x in player.exposed:
            if x.is_pong():
                y = x.mentu_id()
                cpungs[y//16,y%16]-=1
        if not player.is_tsumo() :
            a = player.agari_tile
            fq = player.hand_freq_array()
            if fq[a] == 3 and cpungs[a//16,a%16] >= 1 :
                cpungs[a//16][a%16] -= 1
        s = np.sum( cpungs )
        if s >= 4:
            return ChineseScore.pong4c
        elif s >= 3 :
            return ChineseScore.pong3c
        elif s >= 2 :
            return ChineseScore.pong2c

    @staticmethod
    def pungs2(player,mentu):
        if mentu["type"] != "normal":
            return None
        pungs = mentu["data"][0]
        if np.sum(pungs) >= 4 :
            return ChineseScore.allpung

    @staticmethod
    def steps(player,mentu):
        if mentu["type"] != "normal":
            return None
        chows = mentu["data"][1]
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

    @staticmethod
    def shifted(player,mentu):
        if mentu["type"] != "normal":
            return None
        pungs = mentu["data"][0]
        for c in range(3):
            for i in range(1,8):
                if pungs[c,i] == 0 :
                    continue
                if pungs[c,i+1] > 0 and pungs[c,i+2] > 0 :
                    if pungs[c,i+3]>0 :
                        return ChineseScore.pong4sh
                    else:
                        return ChineseScore.pong3sh
        for r in tricolor:
            for i in range(9):
                if pungs[0,i+r[0]] > 0 and pungs[1,i+r[1]] > 0 and pungs[2,i+r[2]] > 0:
                    return ChineseScore.pong3msh
        return None

    @staticmethod
    def samepong(player,mentu):
        if mentu["type"] != "normal":
            return None
        q = mentu["data"][0]
        cnt = np.sum( q > 0 , axis = 0 )
        if ( cnt >= 3 ).any() :
            return ChineseScore.pong3s
        if ( cnt >= 2 ).any() :
            return ChineseScore.pong2s

    @staticmethod
    def samechow(player,mentu):
        if mentu["type"] != "normal":
            return None
        q = mentu["data"][1]
        if ( q >= 4 ).any():
            return ChineseScore.chow4s
        if ( q >= 3 ).any():
            return ChineseScore.chow3s
        cnt = np.sum( q > 0 , axis = 0 )
        if ( cnt >= 3 ).any() :
            return ChineseScore.chow3ms

    @staticmethod
    def twochows(player,mentu):
        if mentu["type"] != "normal":
            return None
        chows = mentu["data"][1]
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

#print( list( filter( lambda x: len(x)>0 and x[0]!="_" , dir(ChineseScore) )) )
# sc = ScoreCalculation(checker=ChineseScore)
# print(len( sc.yaku ))
# print( ",".join( map( lambda x: x.chinese_name , sc.yaku ) ) )
import unittest
import agari
def getmentu(str):
    m = string_to_array(str)
    return agari.is_agari(m)


class TestScore(unittest.TestCase):
    __sc__ = ScoreCalculation(ChineseScore)
    def test(self):
        pass

if __name__ == "__main__" :
#    unittest.main()

    print(TestScore.__sc__.calc_score(None, getmentu("123m234p345sEEESS") ) )
    print(TestScore.__sc__.calc_score(None, getmentu("123m456p123789sSS") ) )
    print(TestScore.__sc__.calc_score(None, getmentu("123789123789mWW") ) )
