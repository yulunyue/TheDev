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

class UniFind:
    def __init__(self,r) -> None:
        self.p=dict()
        self.size=dict()
        for v in r:
            self.p[v]=v
            self.size[v]=1

    def merge(self,f,t):
        f1=self.find(f)
        t1=self.find(t)
        if f1==t1:
            return False
        self.p[f1]=t1
        self.size[t1]+=self.size[f1]
        self.size[f1]=0
        return True
    
    def find(self,v):
        if self.p[v]!=v:
            self.p[v]=self.find(self.p[v])
        return self.p[v]
    
    def update(self):
        for k in self.p:
            self.find(k)

    def get_pkeys(self):
        return set(list(self.p.values()))

class Solution:
    def get_cases(self):
        return [
            [3, [[0,1,2],[1,2,4],[2,0,8],[1,0,16]], [[0,1,2],[0,2,5]],[false,true]],
            [5, [[0,1,10],[1,2,5],[2,3,9],[3,4,13]],  [[0,4,14],[1,4,13]],[true,false]],
           
        ]

    def distanceLimitedPathsExist(self, n: int, edgeList: List[List[int]], queries: List[List[int]]) -> List[bool]:
        edgeList.sort(key=lambda v:v[2])
        f=UniFind(range(n))
        ans=[False]*len(queries)
        queries=sorted(enumerate(queries),key=lambda a:a[1][2])
        k=0
        for i,(p,q,d) in queries:
            while k<len(edgeList) and edgeList[k][2]<d:
                f.merge(edgeList[k][0],edgeList[k][1])
                k+=1
            ans[i]=f.find(p)==f.find(q) 
        return ans


    def test(self,*args):
        return self.distanceLimitedPathsExist(*args)
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
                self.log("finish")
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



