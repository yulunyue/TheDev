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
            dict(n=6, edges=[[0, 1], [1, 2], [1, 3], [3, 4], [
                 3, 5]], price=[9, 8, 7, 6, 10, 5], result=24.1),
        ]

    def execute(self, n: int, edges: List[List[int]], price: List[int]) -> int:
        g=[[] for _ in range(n)]
        self.ans=-inf
        for f,t in edges:
            g[f].append(t)
            g[t].append(f)
        def dfs():
            pass

        return self.ans

    def maxOutput(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
