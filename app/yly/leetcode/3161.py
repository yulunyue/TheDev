# from sortedcontainers import SortedList
from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


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


class Solution:
    def get_cases(self):
        return [
            [[[1, 6], [1, 1], [2, 7, 5]], [true]],
            [[[1, 7], [1, 6], [2, 4, 9], [1, 11], [2, 11, 5]], [false, true]],
            [[[1, 1], [1, 11], [1, 4], [1, 8], [2, 13, 7]], [False]],
            [[[1, 3], [2, 4, 2]], [true]],
            [[[1, 2], [2, 3, 3], [2, 3, 1], [2, 2, 2]], [false, true, true]],
            [[[1, 7], [2, 7, 6], [1, 2], [2, 7, 5], [2, 7, 6]], [true, true, false]]
        ]

    def getResults(self, queries: List[List[int]]) -> List[bool]:
        max_id = 5*(10**4)+2
        max_id = 20
        wall_ids = [0, max_id]
        seg_tree = SegTree()

        def set_wall(x):
            l = bisect.bisect_left(wall_ids, x)
            seg_tree.update(x, wall_ids[l], wall_ids[l]-x)
            seg_tree.update(wall_ids[l-1], x, x-wall_ids[l-1])
            wall_ids.insert(l, x)

        def query(x, w):
            if x < w:
                return False
            l = bisect.bisect_left(wall_ids, x)
            return x-wall_ids[l-1] >= w or seg_tree.query(1, wall_ids[l-1]) >= w

        ret = []
        for tp, *args in queries:
            if tp == 1:
                set_wall(*args)
            else:
                ret.append(query(*args))
        return ret

    def check(self, *args):
        pass

    def __init__(self) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s):
        if not self.local_debug or len(self.logs) >= 2048:
            return
        self.logs += " ".join([str(v) for v in s])+"\n"

    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs = ""
            try:
                r = self.local_debug(*case[:-1])
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, case[-1]):
                self.check(*case, r)
                print(case, r)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
