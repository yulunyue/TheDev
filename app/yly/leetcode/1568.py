from sortedcontainers import SortedList
from typing import List,Dict,Optional
from collections import defaultdict, deque,Counter
from itertools import accumulate,product
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf=float("inf")
null=None
true=True
false=False
M=10**9 + 7

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Graph:
    def __init__(self,g) -> None:
        self.g=g
        self.n=len(g)

    def tarjan(self,b):
        low=defaultdict(int)
        vt=defaultdict(int)
        self.ct=1
        edges=[]
        def dfs(n,p=None):
            vt[n]=low[n]=self.ct
            self.ct+=1
            for nv in self.g[n]:
                if p==nv:
                    continue
                if vt[nv]==0:
                    dfs(nv,n)
                    low[n]=min(low[nv],low[n])
                    if vt[n]<low[nv]:
                        edges.append([n,nv])
                else:
                    low[n]=min(low[n],vt[nv])
        
        dfs(b,-1)
        return edges,vt,low

class Solution:
    def get_cases(self):
        return [
            [[[0,1,1],[1,1,1],[1,1,0]],1],
            [[[0,0]],0],
            [[[0,0,0],[0,1,0],[0,0,0]],1],
            [[[1,1]],2],
            [[[1,1],[1,0]],1],
            [[[1,0,1,0]],0],
            [[[1,1,1],[1,0,1],[1,1,1]],2],
            [[[0,1,1,0],[0,1,1,0],[0,0,0,0]],2],
            [[[1,1,0,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,1,1,1,1]],2]
        ]
    
    def minDays(self, grid: List[List[int]]) -> int:
        n=len(grid)
        m=len(grid[0])
        ct=0
        dr=[[0,1],[0,-1],[-1,0],[1,0]]
        g=[[] for _ in range(n*m)]
        s3=0
        for gd in grid:
            s3+=sum(gd)
            self.log(gd)
        if s3==1:
            return 1
        if s3==0:
            return 0
        def dfs(y,x):
            grid[y][x]=2
            p=y*m+x
            for dy,dx in dr:
                ny,nx=y+dy,x+dx
                if ny<0 or nx<0 or ny>=n or nx>=m:
                    continue
                if grid[ny][nx]!=0:
                    p1=ny*m+nx
                    g[p].append(p1)
                if grid[ny][nx]==1:
                    dfs(ny,nx)
        bt=0
        for i in range(n):
            for j in range(m):
                if grid[i][j]!=1:
                    continue
                bt=i*m+j
                dfs(i,j)     
                ct+=1
                if ct==2:
                    return 0
        self.log(g)
        egs,vt,mp=Graph(g).tarjan(bt)
        self.log(egs,vt,mp)
        if not egs:
            return 2
        
        # ct2=defaultdict(int)
        ct3=set(mp.values())
        # for v in mp.values():
        #     ct2[v]+=1
        #     if ct2[v]>=2:
        #         ct3.add(v)
        # self.log(ct3)
        if len(ct3)>2:
            return 1
        return 2


    def check(self,*args):
        pass

    def __init__(self) -> None:
        self.local_debug=getattr(self,sys.argv[-1],None)
        if self.local_debug is None:
            print(sys.argv[-1],"not find")
    logs = ""
    def log(self, *s):
        if not self.local_debug or len(self.logs)>=2048:
            return
        self.logs += " ".join([str(v) for v in s])+"\n"
    
    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs=""
            try:
                r=self.local_debug(*case[:-1])
            except Exception as e:
                import traceback
                traceback.print_exc()
                r=None
            if not self.diff(r,case[-1]):
                self.check(*case,r)
                print(case,r)
                print(self.logs)
                break
    def diff(self,a,b):
        if isinstance(a,float) and isinstance(b,float):
            return "%.2f"%(a)=="%.2f"%(b)
        return a==b

    



      

if __name__ == '__main__':
    Solution().run()



