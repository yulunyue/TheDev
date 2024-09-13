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


class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(n = 6, edges = [[0,1],[1,2],[1,3],[3,4],[3,5]], price = [9,8,7,6,10,5],result=24),
        ]

    def execute(self, n: int, edges: List[List[int]], price: List[int]) -> int:
        RECORD_ENABLE = True
        if n==1:
            return 0
        g=[[] for _ in range(n)]
        for f,t in edges:
            g[f].append(t)
            g[t].append(f)
        self.ans=0
        def dfs(i,p):
            ret=0
            for n in g[i]:
                if n==p:
                    continue
                ret=max(get_max(n,i),ret)
            return ret+price[i]
        dfs(0,-1)
        return self.ans
    def maxOutput(self, *args,**kg):
        return self.execute(*args,**kg)


if __name__ == '__main__':
    Solution().run()
