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
            dict(receiver = [2,0,1], k = 4,result=6)
        ]

    def execute(self, receiver: List[int], k: int) -> int:
        m=k.bit_length()-1
        pc=[[[p,p]]+[None]*m for p in receiver]
        for i in range(m):
            for x in range(len(receiver)):
                p,s=pc[x][i]
                pp,ss=pc[p][i]
                pc[x][i+1]=[pp,s+ss]
        ret=0
        for j in range(len(receiver)):
            tmp=x=j
            for i in range(m+1):
                if k&(1<<i):
                    x,c=pc[x][i]
                    tmp+=c
            ret=max(ret,tmp)
        return ret



    def getMaxFunctionValue(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
