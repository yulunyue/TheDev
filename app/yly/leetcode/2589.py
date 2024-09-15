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
    from app.yly.leetcode.manage import SolutionBase
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


class SegTreeNode:
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''

    def __init__(self, idx, l, r, value=0) -> None:
        self.idx = idx
        self.l = l
        self.r = r
        self.value = value
        self.lasy = 0
        self.left: SegTreeNode = None
        self.right: SegTreeNode = None

    def update(self, l, r, value):
        if l <= self.l and self.r <= r:
            pass


class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(tasks=[[2, 3, 1], [4, 5, 1], [1, 5, 2]], result=2)
        ]

    def execute(self, tasks: List[List[int]]) -> int:
        RECORD_ENABLE = True

        root = SegTreeNode(1, 1, 2000)
        for s, e, d in tasks:
            root.update(s, e, d)

    def findMinimumTime(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
