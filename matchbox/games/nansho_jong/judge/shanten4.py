try:
    from .util import *
except:
    from util import *


def randomhand(length=14, tile_list=None):
    if tile_list is None:
        tile_list = [1, 2, 3, 4, 5, 6, 7, 8, 9,
                     17, 18, 19, 20, 21, 22, 23, 24, 25,
                     33, 34, 35, 36, 37, 38, 39, 40, 41,
                     49, 50, 51, 52, 53, 54, 55] * 4
    deck = np.array(tile_list)  # + [56] * 8 )
    np.random.shuffle(deck)
    return np.bincount(deck[0:length], minlength=64)

def suitwise_maisu13k(ary):
    tmp = np.zeros(16, dtype=np.int16)
    for i in range(10):
        if ary[i] > 0:
            tmp[i+3] = 1 + tmp[i]
        tmp[i+1] = max(tmp[i], tmp[i+1])
    return np.max(tmp)

def suitwise_space13k(ary):
    res = suitwise_maisu13k(ary)
    if res == 2 :
        if (( ary[3] > 0 and (ary[7] > 0 or ary[8] > 0 ) ) or 
            ( ary[2] > 0 and ary[7] > 0) ) :
            return res,0
    return res,3 - res


class ShantenCalculator:
    hnnx = np.ndarray(7, dtype=np.int32)
    hnnx[0:4] = np.roll(range(0, 4), 1)
    hnnx[4:7] = np.roll(range(4, 7), -1)

    def __init__(self, tiles,wild=[]):
        self.tile_cnt = tiles
        self.tmp_points = np.zeros((6, 2), dtype=np.int8)
        self.memo = np.full((5, 6, 2), fill_value=-99)
        self.memo[0, 0, 0] = 0
        self.parts = 0
        self.points = 0
        self.pair = 0

    def shanten(self,exposed=0):
        if exposed == 0:
            s13 = self.shanten_13futo()
            s7p = self.shanten_7pairs()
            snm = self.shanten_normal()
            return min(snm,s13.s7p)
        else:
            return self.shanten_normal(exposed)

    def shanten_all(self,exposed=0):
        if exposed == 0:
            s13 = self.shanten_13futo()
            s7p = self.shanten_7pairs()
            snm = self.shanten_normal()
            return {"13futo":s13,"7pairs":s7p,"normal":snm}
        else:
            return {"normal":self.shanten_normal(exposed)}

    def wild_shanten(self,wild=[],exposed=0):
        self.tile_except_wild = tiles.copy()
        self.wild_cnt = tiles[wild]
        self.tile_except_wild[wild] = 0

        s13 = self.wild_13futo(wild=wild)
        s7p = self.wild_7pairs(wild=wild)
        snm = self.wild_normal(wild=wild,exposed=exposed)

    def shanten_7pairs(self): #七対(4枚可能)
        fq = np.bincount(self.tile_cnt,minlength=5)
        if ALLOW_FOUR_IN_7PAIRS :
            return 6 - (np.sum(fq[2:]) + np.sum(fq[4:]))
        else:
            res = 6 - np.sum(fq[2:])
            ts = np.sum(fq[1:])
            if ts < 7:
                res += 7 - ts
            return res

    def wild_7pairs(self): #七対(4枚可能)
        fq = np.bincount(self.tile_without_wild,minlength=5)
        if ALLOW_FOUR_IN_7PAIRS :
            return 6 - (np.sum(fq[2:]) + np.sum(fq[4:])) - self.wild_cnt
        else:
            raise NotImplementedError()

    def shanten_13futo(self):
        maisu = (suitwise_maisu13k(self.tile_cnt[0:16]) +
                suitwise_maisu13k(self.tile_cnt[16:32]) +
                suitwise_maisu13k(self.tile_cnt[32:48]) +
                np.sum(self.tile_cnt[49:]>0))
        return 13-maisu

    def wild_13futo(self,wild=[]):
        ary = self.tile_without_wild
        ary[ wild ] = 0
        m1 , s1 = suitwise_space13k(ary[0:16])
        m2 , s2 = suitwise_space13k(ary[16:32])
        m3 , s3 = suitwise_space13k(ary[32:48])
        m4 = np.sum(self.tile_without_wild[49:]>0)
        s4 = 7-m4
        space = s1 + s2 + s3 + s4
        wild_cnt = min(space,self.wild_cnt)
        return 13 - (m1+m2+m3+m4) - wild_cnt

    def shanten_normal(self,exposed=0):
        self.left = self.tile_cnt[1:10]
        self.curcolor = 0
        self.memo[self.curcolor+1, :, :] = self.memo[self.curcolor, :, :]
        self._recur_colorwise_num(0, 0)
        self._colorwise_result_apply()

        self.left = self.tile_cnt[16+1:16+10]
        self.curcolor = 1
        self.memo[self.curcolor+1, :, :] = self.memo[self.curcolor, :, :]
        self._recur_colorwise_num(0, 0)
        self._colorwise_result_apply()

        self.left = self.tile_cnt[32+1:32+10]
        self.curcolor = 2
        self.memo[self.curcolor+1, :, :] = self.memo[self.curcolor, :, :]
        self._recur_colorwise_num(0, 0)
        self._colorwise_result_apply()

        self.left = self.tile_cnt[48+1:48+8]
        self.curcolor = 3
        self.memo[self.curcolor+1, :, :] = self.memo[self.curcolor, :, :]
        self._recur_colorwise_honor(0, 0)
        self._colorwise_result_apply()

        self.memo[4 , 5 - exposed:, 0] = -99
        self.memo[4 , 6 - exposed:, 1] = -99
        # print(self.memo)
        return 8 - 2*exposed - np.max(self.memo[4])

    def wild_normal(self,exposed=0,wild=[]):
        ary = self.tile_without_wild
        wild_cnt = self.wild_cnt
        self.left = ary[1:10]
        self.curcolor = 0
        self.memo[self.curcolor+1, :, :] = self.memo[self.curcolor, :, :]
        self._recur_colorwise_num(0, 0)
        self._colorwise_result_apply()

        self.left = ary[16+1:16+10]
        self.curcolor = 1
        self.memo[self.curcolor+1, :, :] = self.memo[self.curcolor, :, :]
        self._recur_colorwise_num(0, 0)
        self._colorwise_result_apply()

        self.left = ary[32+1:32+10]
        self.curcolor = 2
        self.memo[self.curcolor+1, :, :] = self.memo[self.curcolor, :, :]
        self._recur_colorwise_num(0, 0)
        self._colorwise_result_apply()

        self.left = ary[48+1:48+8]
        self.curcolor = 3
        self.memo[self.curcolor+1, :, :] = self.memo[self.curcolor, :, :]
        self._recur_colorwise_honor(0, 0)
        self._colorwise_result_apply()

        self.memo[4 , 5 - exposed:, 0] = -99
        self.memo[4 , 6 - exposed:, 1] = -99
        return 8 - 2*exposed - np.max(self.memo[4]) - self.wild_cnt

    def _colorwise_result_apply(self):
        prev = self.memo[self.curcolor, :, :]
        res = self.memo[self.curcolor+1, :, :]
        for pt in range(6):
            p0 = self.tmp_points[pt, 0]
            p1 = self.tmp_points[pt, 1]
            res[pt:, 1] = np.maximum(
                res[pt:, 1], np.max(prev[:6-pt, :], axis=1) + p1)
            res[pt:6, :] = np.maximum(res[pt:6, :],  prev[:6-pt, :] + p0)
        res[5, 0] = -99
        self.tmp_points[:, :] = 0

    def _colorwise_result(self):
        pr = int(self.pair > 0)
        pt = self.parts
        if self.tmp_points[pt, pr] < self.points:
            self.tmp_points[pt, pr] = self.points

    def _recur_colorwise_honor(self, k, ty):
        hnnx = ShantenCalculator.hnnx
        if k >= 7 or self.parts >= 5:
            self._colorwise_result()
            return
        while self.left[k] == 0:
            k += 1
            if k >= 7:
                self._colorwise_result()
                return
        self.parts += 1
        p1 = self.left[hnnx[k]]
        p2 = self.left[hnnx[hnnx[k]]]
        if ty <= 0 and self.left[k] >= 2:  # AA
            self.pair += 1
            self.points += 1
            self.left[k] -= 2
            self._recur_colorwise_honor(k, 0)
            self.pair -= 1
            self.points -= 1
            self.left[k] += 2
        if ty <= 1 and self.left[k] >= 3:  # AAA
            self.points += 2
            self.left[k] -= 3
            self._recur_colorwise_honor(k, 1)
            self.points -= 2
            self.left[k] += 3
            """
        self.left[k] -= 1
        
        if ty <= 2 and ( p1 > 0 and p2 > 0 ): # ABC
            self.points += 2 
            self.left[ hnnx[k] ] -= 1
            self.left[ hnnx[hnnx[k]] ] -= 1
            self._recur_colorwise_honor(k,2)
            self.points -= 2 
            self.left[ hnnx[k] ] += 1
            self.left[ hnnx[hnnx[k]] ] += 1
        if ty <= 3 and p1 > 0: # AB
            self.points += 1 
            self.left[ hnnx[k] ] -= 1
            self._recur_colorwise_honor(k,3)
            self.points -= 1 
            self.left[ hnnx[k] ] += 1
        if ty <= 4 and p2 > 0: # AC
            self.left[ hnnx[hnnx[k]] ] -= 1
            self.points += 1 
            self._recur_colorwise_honor(k,4)
            self.points -= 1 
            self.left[ hnnx[hnnx[k]] ] += 1
            
        self.left[k] += 1"""
        self.parts -= 1
        self._recur_colorwise_honor(k+1, 0)

    def _recur_colorwise_num(self, k, ty):
        if k >= 9 or self.parts >= 5:
            self._colorwise_result()
            return
        while self.left[k] == 0:
            k += 1
            if k >= 9:
                self._colorwise_result()
                return
        self.parts += 1
        if ty <= 0 and self.left[k] >= 2:  # AA
            self.pair += 1
            self.points += 1
            self.left[k] -= 2
            self._recur_colorwise_num(k, 0)
            self.pair -= 1
            self.points -= 1
            self.left[k] += 2
        if self.pair == 0 and self.parts >= 5:
            self.parts -= 1
            self._colorwise_result()
            return
        if ty <= 1 and self.left[k] >= 3:  # AAA
            self.points += 2
            self.left[k] -= 3
            self._recur_colorwise_num(k, 1)
            self.points -= 2
            self.left[k] += 3
        if ty <= 2 and k+2 < 9 and (self.left[k+1:k+3] > 0).all():  # ABC
            self.points += 2
            self.left[k:k+3] -= 1
            self._recur_colorwise_num(k, 2)
            self.points -= 2
            self.left[k:k+3] += 1
        else:
            if ty <= 3 and k+1 < 9 and self.left[k+1] > 0:  # AB
                self.points += 1
                self.left[[k, k+1]] -= 1
                self._recur_colorwise_num(k, 3)
                self.points -= 1
                self.left[[k, k+1]] += 1
            if ty <= 4 and k+2 < 9 and self.left[k+2] > 0:  # AC
                self.left[[k, k+2]] -= 1
                self.points += 1
                self._recur_colorwise_num(k, 4)
                self.points -= 1
                self.left[[k, k+2]] += 1
        self.parts -= 1
        self._recur_colorwise_num(k+1, 0)


def compare_lex(x, y):
    if (x == y).all():
        return 0
    idx = np.where(x != y)[0][0]
    if x[idx] > y[idx]:
        return -1
    else:
        return 1


def max_lex(x, *args):
    res = x
    for y in args:
        if compare_lex(res, y) > 0:
            res = y
    return res


def shanten_exp(ary, expect=4, atama=True):
    return ShantenCalculator(ary).shanten_all()


def shanten_normal(ary):
    return shanten_exp(ary, expect=4)

if __name__ == "__main__" :
    pass
