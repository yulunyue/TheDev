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
        pass

    def handleQuery(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
