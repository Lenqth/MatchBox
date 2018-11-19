# -*- coding : utf8 -*-

import numpy as np
import sys,os

from functools import total_ordering

from .agent import *
from .structs import *

from .judge.agari import is_agari
from .judge.shanten import shanten
from .judge.scoring import ScoreCalculation,ChineseScore
from .judge.util import *

import asyncio

def to_mentu(hand_pattern,exposed):
    res = []
    for x in exposed:
        res.append(Mentu(x.type,x.head))
    for x in hand_pattern:
        if len(x) == 2 :
            res.append(Mentu(Mentu.ATAMA,x[0]))
        elif x[0] != x[1]:
            res.append(Mentu(Mentu.CONCCHOW,x[0]))
        else:
            res.append(Mentu(Mentu.CONCPUNG,x[0]))
    return res


async def _sleep(n):
    await asyncio.sleep(n)

def to_back(ary):
    return [0]*len(ary)

class Player:
    def __init__(self,game,id):
        self.game = game
        self.id = id
        self.reset()

    def chk_agari(self,game,tile):
        self.agari_tile = tile
        res = is_agari( list_to_array(self.hand+[tile]),exposed_mentu=len(self.exposed) )
        self.agari_tile = None
        self.agari_patterns = res
        return (res is not None)

    def chk_value(self,game,tile,pattern):
        sc = ScoreCalculation(ChineseScore)
        total,yaku = sc.calc_score( to_mentu(pattern,self.exposed) , env = {
                        "prevalent_wind": game.prevalent_wind ,
                        "seat_wind": game.get_seat_wind(self.id),
                        "tsumo":tsumo ,
                        "agari_tile":tile,
                        "deck_left":game.lefttile(),
                        "discarded_tiles": [ p.trash for p in game.players ],
                        "exposed_tiles": [ [ Mentu(x.type,x.head) for x in p.exposed ] for p in game.players ]
                     } )
        return (total,yaku)

    def chk_claim(self,game,tile,apkong):
        res = []
        if self.chk_agari( game , tile  ): #ロン
            res.append( Claim(Claim.RON) )
        if apkong:
            return res
        fq = np.bincount(self.hand,minlength=64)
        a = np.array(self.hand)
        # chow
        if (game.turn+1)%4 == self.id and tile < 48: # number tiles
            if fq[tile-1] > 0 and fq[tile+1] > 0 :
                res.append( Claim( Claim.CHOW , [ np.where(a==tile-1)[0][0] , np.where(a==tile+1)[0][0] , -2 ] ) )
            if fq[tile+1] > 0 and fq[tile+2] > 0 :
                res.append( Claim( Claim.CHOW , [ np.where(a==tile+1)[0][0] , np.where(a==tile+2)[0][0] , -2 ] ) )
            if fq[tile-2] > 0 and fq[tile-1] > 0 :
                res.append( Claim( Claim.CHOW , [ np.where(a==tile-2)[0][0] , np.where(a==tile-1)[0][0] , -2 ] ) )
        # pung
        if fq[tile] >= 2 :
            res.append( Claim( Claim.PUNG , list( np.where(a==tile)[0][0:2] ) + [-2] ) )
        # kong
        if fq[tile] >= 3 :
            res.append( Claim( Claim.MINKONG , list( np.where(a==tile)[0][0:3] ) + [-2] ) )
        return res

    def chk_turn_claim(self,game):
        # apkong
        res = []
        for ex in self.exposed:
            if ex.type == Exposed.PUNG :
                for (p,t) in enumerate(self.hand) :
                    if t == ex.head :
                        res.append( TurnCommand(TurnCommand.APKONG,[p] , ex ) )
                if self.drew == ex.head :
                    res.append( TurnCommand(TurnCommand.APKONG,[-1] , ex ) )

        #conckong
        fq = np.bincount(self.hand,minlength=64)
        a = np.array(self.hand)
        for (t,q) in enumerate(fq) :
            if q >= 4 :
                arr = np.array(self.hand)
                res.append( TurnCommand(TurnCommand.CONCKONG, list(np.where(a == t)[0][0:4]) ) )
            elif q >= 3 and t == self.drew :
                arr = np.array(self.hand)
                res.append( TurnCommand(TurnCommand.CONCKONG, list(np.where(a == t)[0][0:3]) + [-1] ) )

        #tsumo
        if self.drew != None and self.chk_agari( game , self.drew ):
            res.append( TurnCommand(TurnCommand.TSUMO) )
        return res

    def reset(self):
        self.hand = []
        self.trash = []
        self.exposed = []
        self.drew = None
        self.flower = 0

    def get_data(self,viewfrom):
        if viewfrom == self.id :
            return {
                "hand" : self.hand,
                "drew" : self.drew,
                "trash" : self.trash ,
                "exposed" : map(lambda x:x.toDict(),self.exposed) ,
                "flower" : self.flower
            }
        else:
            return {
                "hand" : to_back(self.hand),
                "trash" : self.trash ,
                "exposed" : map(lambda x:x.toDict(),self.exposed) ,
                "flower" : self.flower
            }

    async def turn(self,game):
        comm = self.chk_turn_claim(game)
        async def _subrt():
            return await self.agent.turn_command_async(self,game,comm)
        res = (await Promise.all( [_subrt(),_sleep(0.25)] ) )[0]
        return res

    async def subturn_async(self,game,tile,apkong): # opponent's turn Claim
        comm = self.chk_claim(game,tile,apkong)
        if len(comm) > 0:
            res = await self.agent.command_async(self,game,comm)
            return res
        else:
            return Claim(0)

    def pop_from_hand(self,position):
        import collections
        single = False
        if isinstance(position,collections.Iterable):
            position_list = sorted(list(position),reverse=True)
        else:
            single = True
            position_list = [position]
        res = []
        for x in position_list:
            if x == -1 :
                assert(self.drew is not None)
                res.append( self.drew )
                self.drew = None
            elif x >= 0:
                res.append( self.hand.pop(x) )
        if single :
            return res[0]
        else:
            return res

    def is_tsumo(self):
        return self.game.turn == self.id

    def hand_freq_array(self):
        return list_to_array(self.hand)

    def get_array(self,show_hand=False):
        res = np.zeros( (44,64) ,dtype=np.int16)
        e = np.eye( 64 )
        e[0] = 0
        trp = np.int16( np.pad( self.trash , [0,40-len(self.trash)] , "constant" ,constant_values = 0) )
        res[4:] = e[ trp ]
        if show_hand:
            res[0] = list_to_array(self.hand)
        return res

    def observe(self):
        res = np.zeros( (4,44,64) )
        for i in range(4):
            res[i] = self.game.players[ (i+self.id) % 4].get_array(show_hand=(i==0))
        return res

    def is_done(self):
        return self.game.is_done

    def get_reward(self):
        return self.game.reward[self.id]

    def shanten(self):
        return shanten(list_to_array(self.hand))
