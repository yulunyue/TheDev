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
            dict(n = 4, edges = [[0,1],[0,2],[1,3],[2,3]],result=[[3,1],[2,0]])
        ]


    def execute(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        
        g=[[] for _ in range(n)]
        for f,t in edges:
            g[f].append(t)
            g[t].append(f)
        inds=defaultdict(list)
        for i in range(n):
            inds[len(g[i])].append(i)
        

    def constructGridLayout(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
