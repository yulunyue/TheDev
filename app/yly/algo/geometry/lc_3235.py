

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
    from app.yly.algo.manage import SolutionBase,div,bs,grid
except:
    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            pass

        def watch(self, watch_ins, _type="text", _ins=None, **kg):
            pass

BLUE='blue'
YELLOW='yellow'
class Solution(SolutionBase):
    uri = "https://leetcode.cn/problems/check-if-the-rectangle-corner-is-reachable/description/"
    name = 'leetcode_3235. 判断矩形的两个角落是否可达'
    ui_viee = 'http://1.14.93.140:8888/font/dist//index.html?route=algo&py_module=app.yly.algo.geometry.lc_3235'
    has_view=True
    tags = ['图','几何']
    def get_cases(self):
        return [
            dict(X =5,Y =4,circles =[[5,6,4],[6,4,2],[2,5,4],[3,5,3]],result=False),
            dict(X =6,Y =13,circles =[[1,5,1],[1,5,1],[5,7,1],[3,7,2],[5,5,1],[2,10,1],[2,1,1]],result=False),
            dict(X =3,Y =3,circles =[[2,1000,997],[1000,2,997]],result=True),
            dict(X=4,Y=4,circles=[[5,5,1]],result=True),
            dict(X=3, Y=4, circles=[[2, 1, 1]], result=True),
            dict(X = 3, Y = 3, circles = [[1,1,2]],result=False),
            
        ]
    
    def init(self, X: int, Y: int, circles: List[List[int]], result=None) -> bool:
        self.x = X
        self.y = Y
        self.n = len(circles)
        self.circles = circles
        self.g=[[] for _ in range(self.n+2)]
        self.i=0
      
    def execute(self,**kg):
        LT=self.n
        RB=self.n+1
        self.log('init',LT,RB)
        def dis(x1, x2, y1, y2):
            return (y1-y2) * (y1-y2)+(x1-x2)*(x1-x2)

        def merge(i,j):
            self.log(i,j)
            self.g[i].append(j)
            self.g[j].append(i)

        while self.i<self.n:
            xi, yi, ir = self.circles[self.i]
            lt=dis(xi,yi,0,0)
            y_in=0<=yi<=self.y
            x_in=0<=xi<=self.x
            left_c = xi-ir <= 0 and xi+ir>= 0 and y_in
            right_c = xi-ir <= self.x and xi+ir>= self.x and y_in
            top_c = yi-ir <= self.y and yi+ir>= self.y and x_in
            bottom_c = yi-ir <= 0 and yi+ir>= 0 and x_in
            self.log(self.i,left_c,bottom_c,top_c,right_c)
            if (left_c and bottom_c) or (top_c and right_c):
                return False
            if left_c or top_c:
                merge(LT,self.i)
                # self.log(f'merge LT {self.i}')
            if right_c or bottom_c:
                merge(RB,self.i)
                #self.log(f'merge RB {self.i}')
            for j in range(self.i+1, self.n):
                xj, yj, jr = self.circles[j]
                x1,x2,y1,y2,r1,r2=xi,xj,yi,yj,ir,jr
                flag1=(x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) <= (r1 + r2) * (r1 + r2)
                flag2=x1 * r2 + x2 * r1 < (r1 + r2) * self.x
                flag3=y1 * r2 + y2 * r1 < (r1 + r2) * self.y
                if flag1 and flag2 and flag3:
                    merge(self.i,j)
                    #self.log(f'merge {self.i} {j}')
            self.i+=1
        vis=set()
        def dfs(c):
            vis.add(c)
            for n in self.g[c]:
                if n in vis:
                    continue
                if n==RB or dfs(n):
                    return True
            return False
        return not dfs(LT)




    def main(self):
        w=8
        def sx(v):
            return 400+(v+1)*w
        def sy(v):
            return 500-(v+1)*w
        a1 = lambda: dict(
            childs=[
                dict(
                    type='line',value=[
                        dict(x=sx(0),y=sy(0)),
                        dict(x=sx(0),y=sy(self.y)),
                        dict(x=sx(self.x),y=sy(self.y))
                    ],
                    data=dict(
                        color=YELLOW
                    )
                ),
                dict(
                    type='line',value=[
                        dict(x=sx(self.x),y=sy(self.y)),
                        dict(x=sx(self.x),y=sy(0)),
                        dict(x=sx(0),y=sy(0)),
                    ],
                    data=dict(
                        color=BLUE
                    )
                )
            ]+[
                dict(type='circle',x=sx(x),y=sy(y),value=w*r) 
                for x,y,r in self.circles
            ]
        )
        b1 = lambda:f'{self.i}'
        return grid(a1,b1)

    def canReachCorner(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
