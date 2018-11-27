

import unittest
import agari
from util import *
from scoring import ChineseScore
import sys,os

def testyaku(str) : 
    handtiles,exposed,tsumo = string_to_list_ex(str)
    env = {
        "prevalent_wind": -1 ,
        "seat_wind": -1,
        "tsumo":tsumo ,
        "deck_left":11,
        "discarded_tiles": [],
        "exposed_tiles": []
    }
    return ChineseScore.judge( handtiles,exposed,env )
#testyaku("111m *NNN 444p 99p 77m 7m!")
#sys.exit()

class TestScore(unittest.TestCase):

    def assertYaku( self , s,q ):
        sc,y,sc2 = testyaku(s)
        yn = set( [ x.chinese_name for x in y ] )
        if yn == set(q) :
            pass
        else:
            raise AssertionError(" Hand : %s , Expect : %s , Got : %s " % (s,q,yn))


    def test_001(self):
        self.assertYaku( "7m 258p 369s ESWNGR 1m!" , ["全不靠","不求人"] )
        self.assertYaku( "147m 28p 369s SWNGR 5p" , ["全不靠","組合龍"] )
        self.assertYaku( "7m 258p 369s ESWNGR H" , ["七星不靠"] )
        self.assertYaku( "147m 258p 369s 456m 7s 7s" , ["組合龍","平和","門前清","単調将"] )
        self.assertYaku( "147m 258p 369s 4567m 7m" , ["組合龍","平和","門前清","単調将"] )
        self.assertYaku( "147p 258s 369m RRR N N!" , ["組合龍","五門斉","箭刻","不求人","単調将"] )
    
    def test_006(self):
        self.assertYaku( "111m *NNN 444p 99p 77m 7m!" , ["三暗刻","缺一門","自摸","么九刻","碰碰和"] )
        self.assertYaku( "111m *NNN 444p 99p 77m 7m" , ["双暗刻","缺一門","么九刻","碰碰和"] )
        self.assertYaku( "111m *NNN *444p 99p 77m 7m" , ["缺一門","么九刻","碰碰和"] )

    def test_007(self):
        self.assertYaku( "123m *234m *345m 77p GG 7p!" , ["一色三歩高", "缺一門"] )

    def test_misc(self):
        self.assertYaku( "*678m *123s 44678s SS 4s!"  ,[   ] )
        self.assertYaku( "6m 147s 28p ESWNRGH 9m!"  ,[    ] )
        self.assertYaku( "*567m 55678s 45667p 5p"  ,[    ] )
        self.assertYaku( "*222p *333p 11199m 13s 2s"  ,[    ] )
        self.assertYaku( "*123s *RRR 78s 123p WW 9s"  ,[    ] )
        self.assertYaku( "*123m *123s *444p 11m 22s 1m"  ,[    ] )
        self.assertYaku( "*678p *EEE *WWWWk 4456p 4p"  ,[    ] )
        self.assertYaku( "*RRR 23s 123789p HH 4s"  ,[    ] )
        self.assertYaku( "*567s 234s 2355789p 1p"  ,[    ] )
        self.assertYaku( "*789m *123s 78899s RR 7s"  ,[    ] )
        self.assertYaku( "*456m *234p *456s 2288m 8m!"  ,[    ] )
        self.assertYaku( "*NNN *999m 67m 44s 678p 8m"  ,[    ] )
        self.assertYaku( "*678p 234s 1134445p 1p!"  ,[    ] )
        self.assertYaku( "*456p *789m *567s 5678p 5p"  ,[    ] )
        self.assertYaku( "*HHH *123m *RRRRk 78m EE 6m!"  ,[    ] )
        self.assertYaku( "67m 123456789s 99p 5m!"  ,[    ] )
        self.assertYaku( "12345679m 567s 77p 8m!"  ,[    ] )
        self.assertYaku( "*HHH *345p 57m 11456s 6m!"  ,[    ] )
        self.assertYaku( "*SSS *777s *111m 888s H H!"  ,[    ] )
        self.assertYaku( "*456p 1123478889p 1p!"  ,[    ] )
        self.assertYaku( "123456m 34566s 45p 6p!"  ,[    ] )
        self.assertYaku( "22255m 345p 34s *GGG 2s!"  ,[    ] )
        self.assertYaku( "*123s *567s 88s 55789p 5p"  ,[    ] )
        self.assertYaku( "7m 258p 369s ESWNGR 1m!"  ,[    ] )
                


if __name__ == "__main__":
    from pprint import pprint
    try:
        unittest.main()
    except:
        pass
