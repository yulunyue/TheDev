from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
try:
    from app.yly.algo.manage import SolutionBase
except:
    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def run(self):
            pass
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(nums1=[0, 1, 0, 0, 0, 0],
                 nums2=[14, 4, 13, 13, 47, 18],
                 queries=[[3, 0, 0], [1, 4, 4], [1, 1, 4], [1, 3, 4], [3, 0, 0], [2, 5, 0], [
                     1, 1, 3], [2, 16, 0], [2, 10, 0], [3, 0, 0], [3, 0, 0], [2, 6, 0]],
                 result=[109, 109, 197, 197]),
            dict(nums1=[1, 0, 1], nums2=[0, 0, 0], queries=[
                 [1, 1, 1], [2, 1, 0], [3, 0, 0]], result=[3])
        ]

    def execute(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        RECORD_ENABLE = True
        n = len(nums1)
        oi = [0]*(n*4)
        flip = [False]*(n*4)

        def build(o, l, r):
            if l == r:
                oi[o] = nums1[l]
                return
            m = (l+r)//2
            build(o*2, l, m)
            build(o*2+1, m+1, r)
            oi[o] = oi[o*2]+oi[o*2+1]

        def do(o, l, r):
            oi[o] = r-l+1-oi[o]
            # flip[o]=not flip[o]
            flip[o] = True
        build(1, 0, n-1)

        def update(o, l, r, L, R):
            if L <= l and r <= R:
                do(o, l, r)
                return
            m = (l+r)//2
            if flip[o]:
                do(o*2, l, m)
                do(o*2+1, m+1, r)
                flip[o] = False
            if m >= L:
                update(o*2, l, m, L, R)
            if m < R:
                update(o*2+1, m+1, r, L, R)
            oi[o] = oi[o*2]+oi[o*2+1]
        ret = []
        s = sum(nums2)
        for op, l, r in queries:
            if op == 1:
                update(1, 0, n-1, l, r)
            elif op == 2:
                s += l*oi[1]
            else:
                ret.append(s)
        return ret

    def handleQuery(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
