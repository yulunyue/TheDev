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
             [6, 2, [[1,4],[2,5],[3,6]],[false,false,true]]
        ]

    def areConnected(self, n: int, threshold: int, queries: List[List[int]]) -> List[bool]:
        ret = []
        u=UniFind(range(n+1))
        
        for t in range(threshold+1,(n//2)+1):
            for j in range(1,(n//t)+1):
                u.merge(t,t*j)
        # self.log(u.p)
        for f,t in queries:
            ret.append(u.find(f)==u.find(t))
        return ret


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



