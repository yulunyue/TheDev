from app.yly.algo.manage import SolutionBase,View
from common.algo.graph import GraphNode
from typing import Dict,List
from functools import lru_cache
from collections import defaultdict
import bisect
MOD=(10**9)+7
inf = float("inf")
class Node(GraphNode):
    pass
class Solution(SolutionBase):
    uri='https://codeforces.com/problemset/problem/81/E'
    def get_cases(self):
        return [
            dict(input='''5
5 2
3 2
5 1
2 1
4 2''',result='''2 2
5 3
2 4''')
        ]
    
    def get_watch(self):
        return [
            View("graph")
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


    def init(self, *args, **kwargs):
        self.n=self.i1()
        self.graph = Node().init()
        for i in range(self.n):
            self.graph.add_edge(i)
            self.graphlove_id,sex_type)
        return super().init(*args, **kwargs)

    def exec(self):

        self.c=[[] for _ in range(self.n)]

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