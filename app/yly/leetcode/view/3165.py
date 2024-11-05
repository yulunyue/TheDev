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
    from app.yly.manage import SolutionBase, to_json
except:
    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def run(self):
            pass

    def to_json(v):
        return v
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class SegTreeNode:
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''

    def __init__(self, l, r, idx=1, default_value=0) -> None:
        self.idx = idx
        self.l = l
        self.r = r
        self.m = (l+r)//2
        self.default_value = default_value
        self.todo = 0
        self.f00 = self.f01 = self.f10 = self.f11 = 0
        self._left: SegTreeNode = None
        self._right: SegTreeNode = None

    @property
    def left(self):
        if not self._left:
            self._left = SegTreeNode(
                self.l, self.m, self.idx*2, self.default_value)
        return self._left

    @property
    def right(self):
        if not self._right:
            self._right = SegTreeNode(
                self.m+1, self.r, self.idx*2+1, self.default_value)
        return self._right

    def query(self, l, r):
        if l <= self.l and self.r <= r:
            return self.f11
        self.down()
        res = 0
        if self.m < r:
            res += self.right.query(l, r)
        if self.m >= l:
            res += self.left.query(l, r)
        return res

    def update(self, l, r, value):
        if l <= self.l and self.r <= r:
            self.do(value)
            return
        self.down()
        if self.m < r:
            self.right.update(l, r, value)
        if self.m >= l:
            self.left.update(l, r, value)
        self.up()

    def do(self, v):
        self.f11 = max(v, 0)

    def down(self):
        if self.todo:
            self.left.do(self.todo)
            self.right.do(self.todo)
            self.todo = 0

    def up(self):
        self.f00 = max(self.left.f00+self.right.f10,
                       self.left.f01+self.right.f00)
        self.f01 = max(self.left.f00+self.right.f11,
                       self.left.f01+self.right.f01)
        self.f11 = max(self.left.f10+self.right.f11,
                       self.left.f11+self.right.f01)
        self.f10 = max(self.left.f10+self.right.f10,
                       self.left.f11+self.right.f00)

    def to_json(self):
        ret = dict(
            title=f"{self.f00},{self.f01},{self.f11},{self.f10}",
            childs=[],
            type="tree"
        )
        if self._left:
            ret['childs'].append(self._left.to_json())
        if self._right:
            ret['childs'].append(self._left.to_json())
        return ret


class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(nums=[3, 5, 9], queries=[[1, -2], [0, -3]], result=21)
        ]

    def init(self, nums: List[int], queries: List[List[int]]) -> int:
        self.nums = nums
        self.queries = queries
        self.n = len(self.nums)
        self.t = SegTreeNode(0, self.n-1)
        self.ans = 0

    def execute(self):
        for i, v in enumerate(self.nums):
            self.t.update(i, i, v)

        for idx, value in self.queries:
            self.t.update(idx, idx, value)
            self.ans += self.t.query(0, self.n-1)
        return self.ans % M

    def maximumSumSubsequence(self, *args, **kg):
        self.init(*args, **kg)
        return self.execute()

    def record(self):
        return dict(childs=[to_json(self.t)])


if __name__ == '__main__':
    Solution().run()
