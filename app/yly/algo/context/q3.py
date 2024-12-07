

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
MOD = (10**9)+7
try:
    from app.yly.algo.manage import SolutionBase,Node,View

except:
    def fmax(a,b,*args):return a if a>b else b
    def fmin(a,b,*args):return a if a<b else b
    class SolutionBase:
        DEV = False
        
        def input(self):
            return input()

        def i1(self):
            return int(self.input())
        
        def il(self,n):
            return [[int(v) for v in self.input().split(' ')] for _ in range(n)]
        
        def log(self, *args, **kwargs):
            pass

        def init(self,*args,**kwargs):
            pass
        
        def execute(self, *args, **kwargs):
            pass

        def exec(self):
            pass

        def run(self):
            print(self.exec())

def prime_flags(max_v):
    ret = [None]*max_v
    for i in range(2, max_v):
        if ret[i] == False:
            continue
        ret[i] = True
        for j in range(i+i, max_v, i):
            ret[j] = False
    return ret
  
PF=prime_flags(10001)

class Solution(SolutionBase):
    uri = ""
    gameid = ''
    name = ''
    tags = []
    has_view = False
    def get_cases(self):
        return [
            dict(n = 17, m = 72,result=-1),
            dict(n = 10, m = 12,result=85),
        ]
    
    def execute(self, n: int, m: int) -> int:
        
        ms = [int(v) for v in str(m)]
        cflag=[10**(len(ms)-i-1) for i in range(len(ms))]
        start = n
        dist = defaultdict(lambda: float('inf'))
        dist[start] = start
        q = [(start, start)]
        while q:
            cost, u = heapq.heappop(q)
            if cost > dist[u]:
                continue
            self.log(cost,u)
            for i in range(len(ms)):
                for j in [1,-1]:
                    v = u+j*cflag[i]
                    if (v // cflag[i])%10==0:
                        continue
                    if PF[v] or v<0:
                        continue
                    target = cost + v
                    if v == m:
                        return target 
                    if target < dist[v]:
                        dist[v] = target
                        heapq.heappush(q, (dist[v], v))
            

        return -1

    
    def minOperations(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute(*arg, **kg)


if __name__ == '__main__':
    Solution().run()
