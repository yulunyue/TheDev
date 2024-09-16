
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

    def __init__(self, idx, l, r, default_value=0) -> None:
        self.idx = idx
        self.l = l
        self.r = r
        self.m = (l+r)//2
        self.default_value = default_value
        self.value = default_value
        self.lasz = 0
        self._left: SegTreeNode = None
        self._right: SegTreeNode = None

    @property
    def left(self):
        if not self._left:
            self._left = SegTreeNode(
                self.idx*2, self.l, self.m, self.default_value)
        return self._left

    @property
    def right(self):
        if not self._right:
            self._right = SegTreeNode(
                self.idx*2+1, self.m+1, self.r, self.default_value)
        return self._right

    def query(self, l, r):
        if l <= self.l and self.r <= r:
            return self.value
        if self.m >= r:
            return self.left.query(l, r)
        if self.m < l:
            return self.right.query(l, r)
        return self.left.query(l, r)+self.right.query(l, r)

    def update_one(self, pos, value):
        if self.l == pos and self.r == pos:
            self.value = value
            return
        if pos <= self.m:
            self.left.update_one(pos, value)
        else:
            self.right.update_one(pos, value)
        self.up()

    def up(self):
        self.value = self.left.value+self.right.value
