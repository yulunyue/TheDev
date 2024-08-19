
from collections import defaultdict


class IntervalTree:
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


class SegTree:
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''

    def __init__(self, size, *args, default_value=None) -> None:
        self.size = size
        self.default_value = float(
            "inf") if default_value is None else default_value
        self.args = args
        self.init()

    def build(self, o=1, l=0, r=None):
        if r is None:
            r = self.size
        m = (l+r)//2
        self.build(o*2, l, m)
        self.build(o*2+1, m+1, r)
        self.merge(o)

    def update_one(self, i, v=None, o=1, l=0, r=None):
        if r is None:
            r = self.size
        m = (l+r)//2
        if i <= m:
            self.update_min(i, v, o*2, l, m)
        else:
            self.update_min(i, v, o*2+1, m+1, r)
        self.merge(o)

    def merge(self, o):
        pass

    def init(self):
        self.store = [self.default_value]*(self.size*4)
        self.lazy = [self.default_value]*(self.size*4)

    def push_lazy(self, i, fun):
        if self.lazy[i] != self.default_value:
            self.lazy[i*2] = fun(self.lazy[i], self.lazy[i*2])
            self.lazy[i*2+1] = fun(self.lazy[i], self.lazy[i*2+1])
            self.store[i*2] = fun(self.lazy[i], self.store[i*2])
            self.store[i*2+1] = fun(self.lazy[i], self.store[i*2+1])
            self.lazy[i] = self.default_value

    def update_min_dp(self, o, l, r, L, R, v):
        if l <= L and R <= r:
            self.lazy[o] = v
            self.store[o] = v
            return
        mid = (L+R)//2
        self.push_lazy(o, lambda a, b: min(a, b))
        if l <= mid:
            self.update_min_dp(o*2, l, r, L, mid, v)
        if r >= mid+1:
            self.update_min_dp(o*2+1, l, r, mid+1, R, v)
        self.store[o] = max(self.store[o*2], self.store[o*2+1])

    def info(self):
        ret = dict(lazy=dict(), store=dict())
        for key in ret.keys():
            for i, v in enumerate(getattr(self, key)):
                if v != self.default_value and v is not None:
                    ret[key][i] = v
        return ret

    def query_min_dp(self, o, l, r, L, R):
        if l <= L and R <= r:
            return self.store[o]
        mid = (L+R)//2
        ret = float("inf")
        self.push_lazy(o, lambda a, b: min(a, b))
        if l <= mid:
            ret = min(self.query_min_dp(o*2, l, r, L, mid), ret)
        if r >= mid+1:
            ret = min(self.query_min_dp(o * 2+1, l, r, mid+1, R), ret)
        return ret

    def query_min(self, l, r):
        return self.query_min_dp(1, l, r, 0, self.size)

    def update_min(self, l, r, v):
        return self.update_min_dp(1, l, r, 0, self.size, v)

    def update_max(self, l, r, v):
        self.update_min(l, r, -v)

    def query_max(self, l, r):
        return -self.query_min(l, r)
