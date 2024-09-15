
from collections import defaultdict


class IntervalTreeNode:
    '''
                    16
        8
    4        12            20
  2   6   10    14     18
 1 3 5 7 9 11 13  15 17  19  21
    '''

    def __init__(self, size, default_value) -> None:
        self.array = [default_value]*size
        self.size = size

    def update_value(self, l, v):
        while l < self.size:
            self.array[l] = v(self.array[l])
            l += l & -l

    def query_value(self, l, f, init_value):
        ret = init_value
        while l > 0:
            ret = f(ret, self.array[l])
            l -= l & -l
        return ret

    def query_sum(self, l):
        return self.query_value(l, lambda a, b: a+b, 0)

    def add_value(self, l, v):
        self.update_value(l, lambda a: a+v)


class SegTreeNode:
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''

    def __init__(self, idx, l, r, value) -> None:
        self.idx = idx
        self.l = l
        self.r = r
        self.value = value
        self.lasy = 0

    def update_value(self, l, r):
        pass
