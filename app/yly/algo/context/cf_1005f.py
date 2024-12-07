

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
try:
    from app.yly.algo.manage import SolutionBase,View

except:
    class SolutionBase:
        def input(self):
            return input()    
        
        def i1(self):
            return int(self.input())
        
        def il(self):
            return [int(v) for v in self.input().split(' ')]
          
        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass
        
        def init(self,*args,**kwagrs):
            pass
        
        def exec(self,*args,**kwargs):
            pass

        def run(self):
            self.init()
            print(self.exec())

CASE2 = '''
4 6 3
1 2
2 3
1 4
4 3
2 4
1 3
'''
RESULT2='''2
111100
110110'''
CASE1 ='''
4 4 3
1 2 
2 3
1 4
4 3
'''
RESULT1='''2
1110
1011'''

class Graph:
    def __init__(self):
        self.g = defaultdict(list)

    def add_edge(self,y,x):
        self.g[x].append(y)
        self.g[y].append(x)  # 建树
    
    def load_from_edges(self,edges):
        self.edges=edges
        for x, y in edges:
            self.add_edge(x,y)
        return self
    
    def to_view(self):
        return dict(data=dict(
            g=dict(self.g)
        ))
    
    def __str__(self):
        return str(self.g)

class Solution(SolutionBase):
    _uri = "https://codeforces.com/problemset/problem/1005/F"
    _gameid = ''
    '''
    给定一个图
    '''
    _has_view=True
    def get_cases(self):
        return [
            dict(input=CASE2,result=RESULT2),
            dict(input=CASE1,result=RESULT1),
        ]
    
    def init(self,*arg,result=0,**kwargs):
        self.root=Graph()
        self.n,self.m,self.k=self.il()
        self.us=[]
        self.vs=[]
        self.dis = [-1]*self.n
        self.dis[0]=0
        self.g=[[] for _ in range(self.n)]
        self.dq=[0]*self.n
        self.l,self.r=0,1
        for i in range(self.m):
            f,t=self.il()
            self.us.append(f-1)
            self.vs.append(t-1)
            self.g[f-1].append(i)
            self.g[t-1].append(i)
            self.root.add_edge(f-1,t-1)

    def get_watch2(self):
        return [
            View(key='root').graph()
        ]
    def exec(self,*args,**kwagrs):
        pass

    def exec2(self,*args,**kwargs):
        ret=[]
        q=[0]
        p=defaultdict(list)
        vt={0}
        tmp=['0']*self.m
        ans2=[]
      
        while q:
            tmp=q
            q=[]
            for u in tmp:
                vt.add(u)
                for v,idx in self.g[u]:
                    if v in vt:
                        continue
                    p[v].append(u)
                    tmp[idx]='1'
                    q.append(v)
                    tmp[idx]='0'
        ans=1   
        for v in p.values():
            ans*=len(v)
  
        self.log(p)
        ret.append(str(ans))
        return "\n".join(ret)



if __name__ == '__main__':
    Solution().run()
