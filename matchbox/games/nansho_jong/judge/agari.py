# -*- coding: utf-8 -*-

try:
    from .util import *
    from .config import *
except:
    from util import *
    from config import *

import numpy as np
import functools
import itertools


def agari_7pairs(ary, exposed_mentu=0, wilds=[]):
    if exposed_mentu > 0:
        return None
    fq = np.bincount(ary, minlength=5)
    if fq[2] == 7:
        return True
    if ALLOW_FOUR_IN_7PAIRS and (fq[2] + fq[4] * 2) == 7:
        return True
    return None


def suitwise_maisu13k(ary):
    tmp = np.zeros(16, dtype=np.int16)
    for i in range(10):
        if ary[i] > 0:
            tmp[i+3] = 1 + tmp[i]
        tmp[i+1] = max(tmp[i], tmp[i+1])
    return np.max(tmp)


def shanten_13k(ary, exposed_mentu=0, wilds=[]):
    maisu = (suitwise_maisu13k(ary[0:16]) +
             suitwise_maisu13k(ary[16:32]) +
             suitwise_maisu13k(ary[32:48]) +
             np.sum(ary[49:]>0))
    return 13-maisu
    
#14不塔


def agari_13k(ary, exposed_mentu=0, wilds=[]):
    if exposed_mentu > 1:
        return None
    if shanten_13k(ary) == -1 :
        return True
    return None



#南昌麻雀では字牌の順子がある



FIVES = np.array( [ ( 5**(i-1) if 1 <= i <= 9 else 0 ) for i in range(16)] )

if ORTHODOX_MODE:
    def __to_number(ary):
        return np.dot( ary , FIVES )
else:
    def __to_number(ary):
        nz = ary.nonzero()[0]
        if np.max(ary) <= 4 and ( (1 <= nz) & (nz <= 9) ).all():
            return None
        return np.dot( ary , FIVES )

_colorwise_parts_memory = np.full( (5**9*2) , None , dtype=np.object )
def _colorwise_parts_cached(ary,is_number=True):
    idx = __to_number(ary)
    isn = 1 if is_number else 0
    if idx == None:
        return _colorwise_parts(ary,is_number=is_number)
    r = _colorwise_parts_memory[ (idx << 1) | isn ]
    if r is None :
        #print("CACHE MISS : {0} {1} ({2})".format(ary,isn,idx))
        v = _colorwise_parts(ary,is_number=is_number)
        _colorwise_parts_memory[(idx << 1) | isn] = v
        v.flags.writeable = False
        return v
    else:
        #print("CACHE HIT : {0} {1} ({2})".format(ary,isn,idx))
        return r

def all_cache_calculation():
    ary = np.zeros( 16 , dtype = np.int16)
    i = 0
    t = 0
    for q in itertools.product( *( [[0,1,2,3,4]]*9) ):
        i += 1
        if i > 100000:
            t += i
            print(t)
        if np.sum(q) > 14 :
            continue
        ary[1:10] = q
        _colorwise_parts_cached(ary,False)
        _colorwise_parts_cached(ary,True)

def _colorwise_parts(ary,is_number=True):
    max_mentu = 0
    res_pair = (0, 0)
    res = (0, 0)
    def _colorwise_parts_internal(k,ty,left,p3,p2,pair):
        nonlocal res, res_pair
        if k>9 or p3 + p2 >= 5 :
            if pair:
                if res_pair < (p3, p2):
                    res_pair = (p3, p2)
            else:
                if res < (p3, p2):
                    res = (p3, p2)
            return
        if left[k] > 0:
            if ty <= 0 and left[k] >= 2 :
                left[k] -= 2
                _colorwise_parts_internal(k,0,left,p3,p2 + 1,1)
                left[k] += 2
            if p3 + p2 >= 4 and pair == 0 :
                return
            if ty <= 1 and left[k] >= 3 :
                left[k] -= 3
                _colorwise_parts_internal(k,1,left,p3+1,p2,pair)
                left[k] += 3
            if is_number :
                if ty <= 2 and (left[k:k+3] > 0).all():
                    left[k:k+3] -= 1
                    _colorwise_parts_internal(k,2,left,p3+1,p2,pair)
                    left[k:k+3] += 1
                else:
                    if ty <= 3 and is_number and left[k+1] > 0:
                        left[ [k,k+1] ] -= 1
                        _colorwise_parts_internal(k,3,left,p3,p2+1,pair)
                        left[ [k,k+1] ] += 1
                    if ty <= 4 and is_number and left[k+2] > 0:
                        left[ [k,k+2] ] -= 1
                        _colorwise_parts_internal(k,4,left,p3,p2+1,pair)
                        left[ [k,k+2] ] += 1
        _colorwise_parts_internal(k+1,0,left,p3,p2,pair)
    defdat = np.copy(ary)
    _colorwise_parts_internal(0,0,defdat,0,0,0)
    return res, res_pair

def shanten_exp(ary,expect=4,atama=True):
    res = [
        _colorwise_parts_cached(ary[0:16]),
        _colorwise_parts_cached(ary[16:32]),
        _colorwise_parts_cached(ary[32:48]),
        _colorwise_parts_cached(ary[48:64],is_number=False)
    ]

    return expect*2 - mv

def agari_normal(ary, exposed_mentu=0,wilds=[]):
    if exposed_mentu > 4:
        return None
    r = expect_mentu(ary, expect=4-exposed_mentu)
    if r is not None:
        return r
    return None

def is_agari(ary, exposed_mentu=0):
    assert(0 <= exposed_mentu <= 4)
    res = []
    if exposed_mentu == 0:
        r = agari_13k(ary, exposed_mentu)
        if r is not None:
            return [{"type": "13futo", "data": r}]
        r = agari_7pairs(ary, exposed_mentu)
        if r is not None:
            res.append({"type": "7pairs", "data": r})
    if r is not None:
        res.extend(
            map(lambda x: {"type": "normal", "data": x[0], "atama": x[1]}, r))
    if len(res) == 0:
        return None
    return res


class Agari:
    def __init__(self):
        pass

    def is_agari(ary, expose=[]):
        pass


def to_array(man="", pin="", sou="", ji=""):
    res = np.zeros(64, dtype=np.int16)
    for c in man:
        res[int(c)] += 1
    for c in pin:
        res[int(c)+16] += 1
    for c in sou:
        res[int(c)+32] += 1
    # "eswnhrg"
    for c in ji:
        res[int(c)+48] += 1
    return res


if __name__ == "__main__":
    #    print( contain_knit(knithand) )
    from pprint import pprint
    #print( _colorwise_mentsu( [0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0] ) )
    #print( expect_mentu(string_to_array("55678s455667p"),expect=3) )
    #pprint( is_agari( string_to_array("123123m345789s55p") )[0]["data"].shape )
    # unittest.main()
