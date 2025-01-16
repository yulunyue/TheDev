from app.yly.algo.manage import SolutionBase,View,np
from typing import Dict,List
from functools import lru_cache
from collections import defaultdict
import bisect
MOD=(10**9)+7
inf = float("inf")
class Node:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def lt(self,b):
        return self.y<b.y if self.x==b.x else self.x<b.x
    
    def add(self,b):
        return Node(self.x+b.x,self.y+b.y)

    def sub(self,b):
        return Node(self.x-b.x,self.y-b.y)

class Solution(SolutionBase):
    uri='https://www.luogu.com.cn/problem/CF81E'
    def get_cases(self):
        return [

        ]
    
    def calc(self,u):
        pass
    def solve(self,u):
        while not self.v[u]:
            self.v[u]=1
            u=self.in_id[u]
        r = Node(0,0)
        for i in range(2):
            self.rt=u
            self.calc(u)


    def exec(self):
        self.n=self.i1()
        self.in_id=[None]*self.n
        self.g=[0]*self.n
        self.rt=0
        self.s=[0]*self.n
        self.v=[0]*self.n
        self.node=[]
        self.p:List[Node]=[]
        self.q:List[Node]=[]
        self.ans = Node(0,0)
        self.c=[[] for _ in range(self.n)]
        for i in range(self.n):
            love_id,sex_type=self.il()
            self.in_id[i]=love_id-1
            self.s[i]=sex_type-1
            self.c[love_id-1].append(i)
        for i in range(self.n):
            if not self.v[i]:
                self.solve(i)
        self.output(f'{self.ans.x} {self.ans.y}')
        for p in self.q:
            self.output(f'{p.x} {p.y}')


if __name__=='__main__':
    Solution().run()