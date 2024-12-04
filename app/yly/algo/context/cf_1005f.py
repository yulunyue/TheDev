

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
    from app.yly.algo.manage import SolutionBase

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

CASE1 ='''
4 4 3
1 2 
2 3
1 4
4 3
'''
result1='''2
1110
1011'''
class Solution(SolutionBase):
    _uri = "https://codeforces.com/problemset/problem/1005/F"
    _gameid = ''

    def get_cases(self):
        return [
            dict(input=CASE1,result=result1),
        ]
    
    def init(self,*arg,**kwargs):
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
