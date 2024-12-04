

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
    from app.yly.algo.manage import SolutionBase,div,bp,divh,divv

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

  


class Solution(SolutionBase):
    uri = ""
    gameid = ''
    name = ''
    tags = []
    has_view = False
    def get_cases(self):
        return [

        ]

    def init(self,*args,**kwargs):
        pass

    def xx(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute(*arg, **kg)


if __name__ == '__main__':
    Solution().run()
