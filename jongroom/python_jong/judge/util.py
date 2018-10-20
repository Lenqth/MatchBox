

import numpy as np
import functools
import itertools


YAOCHU = [1,9,16+1,16+9,32+1,32+9,49,50,51,52,53,54,55]

def list_to_array(li):
    res = np.zeros(64  ,dtype=np.int16)
    for x in li:
        res[x] += 1
    return res

def list_to_string(li):
    li = sorted(li)
    m = ""
    p = ""
    s = ""
    c = ""
    cname = " ESWNHRG"
    for x in li:
        if 1 <= x <= 9 :
            m = m + str(x)
        elif 1 <= (x-16) <= 9 :
            p = p + str(x-16)
        elif 1 <= (x-32) <= 9 :
            s = s + str(x-32)
        elif 1 <= (x-48) <= 9 :
            c = c + cname[x-48]
    res = ""
    if m != "" :
        res += m+"m"
    if p != "" :
        res += p+"p"
    if s != "" :
        res += s+"s"
    res += c
    return res

def string_to_list(s):
    res = []
    buff = []
    d = { "E":49 , "S" : 50 , "W":51 , "N":52,"H":53,"R":54,"G":55 }
    for c in s:
        if '0' <= c <= '9':
            buff.append(int(c))
        elif c == "m" :
            res.extend( map(lambda x:x,buff) )
            buff=[]

        elif c == "p" :
            res.extend( map(lambda x:x+16,buff) )
            buff=[]

        elif c == "s" :
            res.extend( map(lambda x:x+32,buff) )
            buff=[]

        else:
            res.append(d[c])
    return res

def string_to_array(s):
    return list_to_array(string_to_list(s))


BITS = np.array( [1<<i for i in range(16)] )

def to_bits(ary):
    aa = np.array(ary)
    aa[aa.nonzero()] = 1
    print(ary,aa)
    return np.sum( aa * BITS[0:len(aa)] )

def from_bits(bits):
    aa = np.zeros(16,dtype=np.int16)
    for i in range(16):
        aa[i] = ( bits >> i ) & 1
    return aa

def randomhand(length=14):
    deck = np.array( [1,2,3,4,5,6,7,8,9,
            17,18,19,20,21,22,23,24,25,
            33,34,35,36,37,38,39,40,41,
            49,50,51,52,53,54,55] * 4 ) # + [56] * 8 )
    np.random.shuffle(deck)
    return np.bincount(deck[0:length],minlength=64)



def to_array(man="",pin="",sou="",ji=""):
    res = np.zeros(64,dtype=np.int16)
    for c in man:
        res[int(c)]+=1
    for c in pin:
        res[int(c)+16]+=1
    for c in sou:
        res[int(c)+32]+=1
    # "eswnhrg"
    for c in ji:
        res[int(c)+48]+=1
    return res

KNITS = np.zeros( (6,64) ,dtype=np.int16 )
KNITMASK = np.zeros( (6,64) ,dtype=np.int16 )
KNITNUMS = np.zeros( (6,16) ,dtype=np.int16 )
def _init_knit():
    m1 = ( 1 | 1 << 3 | 1 << 6 ) << 1
    m2 = m1<<1
    m3 = m1<<2
    for i,v in enumerate(itertools.permutations( ( m1 , m2 , m3 ) )) :
        a , b , c = v
        KNITS[i,0:16] = from_bits(a)
        KNITS[i,16:32] = from_bits(b)
        KNITS[i,32:48] = from_bits(c)
        KNITMASK[i,0:16] += from_bits(a)
        KNITMASK[i,16:32] += from_bits(b)
        KNITMASK[i,32:48] += from_bits(c)
        KNITMASK[i,49:49+7] += 1
        KNITNUMS[i,:] = (KNITMASK[i]).nonzero()[0]
_init_knit()

if __name__ == "__main__" :
    print( list_to_array([0,1,2,3,6,6,9]) )
    print( KNITNUMS )
    print(randomhand())
