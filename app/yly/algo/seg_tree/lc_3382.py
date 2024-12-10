

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
from common.algo.segtree import SegTreeNode

class Solution(SolutionBase):
    uri = "https://leetcode.cn/problems/maximum-area-rectangle-with-point-constraints-ii/description/"
    _has_view=True
    gameid = ''
    def get_cases(self):
        return [
            dict(xCoord =[6,32,6,32,14,8,75,42,72,36,61,70,43,58,26,10,42,22,5,41],yCoord =[62,45,45,62,26,27,68,69,14,71,39,36,62,60,96,76,63,14,45,41],result=442),
            dict(xCoord =list(range(9)),yCoord =list(range(9)),result=-1),
            dict(xCoord =[1,1,3,3,2],yCoord =[1,3,1,3,2],result=-1),
            dict(xCoord = [1,1,3,3], yCoord = [1,3,1,3],result=4),
            dict( xCoord = [1,1,3,3,1,3], yCoord = [1,3,1,3,2,2],result=2)
        ]
    def get_watch(self):
        return [
            View().add_node(
                View("xCoord"),
                View("yCoord"),
                View("ans"),
                View("xss"),
                View("yss"),
                View("querys"),
                View("gp"),
                View("res"),
                View("action"),
                View("result"),
            ),
            View("fenwick",size=36).graph(),
            View("seg",size=36).graph()
        ]
    def init(self, xCoord,yCoord,result=0,**kw) -> int:
        self.ans=result
        self.result=-1
        self.xCoord=xCoord
        self.yCoord=yCoord
        self.n = len(xCoord)
        self.x_mp=defaultdict(list)
        self.y_mp=defaultdict(list)
        self.xss = []
        self.yss = []
        self.querys = []
        self.gp =[]
        self.res = []
        self.seg=SegTreeNode()
        self.fenwick = Fenwick()

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
        
 
        self.res=[[0,0] for _ in range(len(querys))]
        self.seg.set_range(0,len(xss)-1)
        self.fenwick.set_size(len(xss))
        for i in range(len(yss)):
            y,qs=yss[i],gp[i]
            for x in self.y_mp[y]:
                bi = bisect.bisect_left(xss,x)
                self.log(f'add {bi+1}')
                self.fenwick.add_value(bi,1)
                self.seg.add_value(bi,1)
            for qid,c,x1,x2 in qs:
                self.res[qid][0]+=c*self.fenwick.query_sum(x1-1, x2)
                self.res[qid][1]+=c*self.seg.query_sum(x1, x2)
                self.log(f'query {x1+1} {x2+1} {self.res[qid]}')
        for i in range(len(self.res)):
            if self.res[i][1]==4:
                self.result=max(self.result,querys[i][4])
        return self.result

        
    
    def maxRectangleArea(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute(*arg, **kg)


if __name__ == '__main__':
    Solution().run()
