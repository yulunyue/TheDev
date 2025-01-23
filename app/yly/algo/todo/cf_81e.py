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
            dict(input='''5
5 2
3 2
5 1
2 1
4 2''',result='''2 2
5 3
4 2''')
        ]
    
    def calc(self,u,rt):
        self.f[u][0] = self.f[u][1] = Node(0,0)
        self.g[u]=0
        self.v[u]=1
        for v in self.c[u]:
            if v==rt:
                continue
            self.calc(v,rt)
            self.f[u][0]=self.f[u][0].add(self.f[v][1]) 
            t=self.f[v][0].sub(self.f[v][1]).add(Node(1,self.s[u]^self.s[v]))
            if self.f[u][1].lt(t):
                self.f[u][1]=t
                self.g[u]=v
        self.f[u][1]=self.f[u][1].add(self.f[u][0])

    def get(self,u,i,rt):
        for p in self.c[u]:
            if p==rt:
                continue
            if not i or self.g[u] != p:
                self.get(p,1,rt)
            else:
                self.p.append(Node(u,p))
                self.get(p,0,rt)

    def solve(self,u):
        while not self.v[u]:
            self.v[u]=1
            u=self.in_id[u]
        r = Node(0,0)
        for _ in range(2):
            self.calc(u,u)
            if r.lt(self.f[u][1]):
                r=self.f[u][1]
                self.p.clear()
                self.get(u,1,u)
            u=self.in_id[u]
        for p in self.p:
            self.q.append(p)
        self.ans=self.ans.add(r)



    def exec(self):
        self.n=self.i1()
        self.f:List[List[Node]]=[[Node(0,0),Node(0,0)] for _ in range(self.n)]
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
            self.output(f'{p.x+1} {p.y+1}')


if __name__=='__main__':
    Solution().run()