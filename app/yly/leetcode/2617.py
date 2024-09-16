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
            dict(grid = [[3,4,2,1],[4,2,1,1],[2,1,1,0],[3,4,1,0]],result=3)
        ]


    def execute(self, grid: List[List[int]]) -> int:
        RECORD_ENABLE = True
        n,m=len(grid),len(grid[0])
        if n==1 and m==1:
            return 1
        step=1
        q=[[0,0]]
        while q:
            tmp=q
            q=[]
            for i,j in tmp:
                for k in range(j+1,m):
                    if k <= grid[i][j] + j:
                        if i==n-1 and k==m-1:
                            return step+1
                        q.append([i,k])
                for k in range(i+1,n):
                    if k <= grid[i][j] + i:
                        if k==n-1 and j==m-1:
                            return step+1
                        q.append([k,j])
            step+=1

        return -1

    def minimumVisitedCells(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
