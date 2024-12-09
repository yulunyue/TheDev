

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

from app.yly.algo.manage import SolutionBase,View
from common.algo.fenwick import Fenwick


class Solution(SolutionBase):
    uri = "https://leetcode.cn/problems/maximum-area-rectangle-with-point-constraints-ii/description/"
    _has_view=True
    gameid = ''
    def get_cases(self):
        return [
            dict(xCoord =[1,1,3,3,2],yCoord =[1,3,1,3,2],result=-1),
            dict(xCoord = [1,1,3,3], yCoord = [1,3,1,3],result=4),
            dict( xCoord = [1,1,3,3,1,3], yCoord = [1,3,1,3,2,2],result=2)
        ]
    def get_watch(self):
        return [
            View().add_node(
                View("xCoord"),
                View("yCoord"),
                View("xss"),
                View("yss"),
                View("querys"),
                View("gp"),
                View("res"),
                View("action")
            ),
            View("fenwick",size=64).tree()
        ]
    def init(self, xCoord,yCoord,*args,**kw) -> int:
        self.xCoord=xCoord
        self.yCoord=yCoord
        self.n = len(xCoord)
        self.x_mp=defaultdict(list)
        self.y_mp=defaultdict(list)

    def execute(self,*args,**kg):
        yn,xn,pt=dict(),dict(),dict()
        for i in range(self.n):
            y,x=self.yCoord[i],self.xCoord[i]
            self.y_mp[y].append(x)
            self.x_mp[x].append(y)
            pt[y,x]=True

        for y,xs in self.y_mp.items():
            xs.sort()
            for i in range(len(xs)-1):
                xn[y,xs[i]]=xs[i+1]
        
        for x,ys in self.x_mp.items():
            ys.sort()
            for i in range(len(ys)-1):
                yn[ys[i],x]=ys[i+1]

        self.xss=xss=sorted(self.x_mp.keys())
        self.yss=yss=sorted(self.y_mp.keys())
        self.querys=querys = []
        for y1,x1s in self.y_mp.items():
            for i in range(len(x1s)-1):
                x1,x2=x1s[i],x1s[i+1]
                y2 = yn.get((y1,x1),None)
                if (y2,x2) not in pt:
                    continue
                querys.append([
                    bisect.bisect_left(xss,x1),
                    bisect.bisect_left(xss,x2),
                    bisect.bisect_left(yss,y1),
                    bisect.bisect_left(yss,y2),
                    (x2-x1)*(y2-y1)
                ])
        
        self.gp=gp=[[] for _ in range(len(yss))]
        for i,(x1,x2,y1,y2,_) in enumerate(querys):
            if y1>0:
                gp[y1-1].append([i,-1,x1,x2])
            gp[y2].append([i,1,x1,x2])
        
        ans=-1
        self.res=res=[0]*len(querys)
        self.fenwick = Fenwick(len(xss))
        for i in range(len(yss)):
            y,qs=yss[i],gp[i]
            for x in self.y_mp[y]:
                bi = bisect.bisect_left(xss,x)
                self.log(f'add {bi+1}')
                self.fenwick.add_value(bi,1)
            for qid,c,x1,x2 in qs:
                res[qid]+=c*self.fenwick.query_sum(x1-1, x2)
                self.log(f'query {x1+1} {x2+1} {res[qid]}')
        for i in range(len(res)):
            if res[i]==4:
                ans=max(ans,querys[i][4])
        return ans

        
    
    def maxRectangleArea(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute(*arg, **kg)


if __name__ == '__main__':
    Solution().run()
