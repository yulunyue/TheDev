

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

  


class Solution(SolutionBase):
    uri = ""
    gameid = ''
    name = ''
    tags = []
    has_view = False
    def get_cases(self):
        return [
             dict( points = [[1,1],[1,3],[3,1],[3,3],[1,2],[3,2]],result=2),
            dict( points = [[1,1],[1,3],[3,1],[3,3],[2,2]],result=-1),
           

        ]
    
    def execute(self, xCoord,yCoord) -> int:
        # n = len(nums)
        # cty=defaultdict(list)
        # for i,(y,x) in enumerate(points):
        #     cty[y].append(x)
        # for k in cty:
        #     cty[k].sort()
        points = [[yCoord[i],xCoord[i]] for i in range(len(xCoord))]
        vt=set()
        for y,x in points:
            vt.add((y,x))
        self.log(vt)
        def check(x1,x2,y1,y2):
            x1,x2=min(x1,x2),max(x1,x2)
            y1,y2=min(y1,y2),max(y1,y2)
          
            for y,x in points:
                if x==x1 and (y==y1 or y==y2):
                    continue
                if x==x2 and (y==y1 or y==y2):
                    continue
                if x1<=x<=x2 and y1<=y<=y2:
                    return False
            
            return True
        ans = -inf
        for i in range(len(points)):
            y1,x1=points[i]
            for j in range(i+1,len(points)):
                y2,x2=points[j]
                if x1==x2 or y1==y2:
                    continue
                if (y1,x2) not in vt:
                    continue
                if (y2,x1) not in vt:
                    continue
                if check(x1,x2,y1,y2):
                    ans=max(ans,abs(y2-y1)*abs(x2-x1))
          
        return -1 if ans == -inf else ans
    def maxRectangleArea(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute(*arg, **kg)


if __name__ == '__main__':
    Solution().run()
