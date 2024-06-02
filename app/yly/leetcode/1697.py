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

class Solution:
    def get_cases(self):
        return [
             [3, [[0,1,2],[1,2,4],[2,0,8],[1,0,16]], [[0,1,2],[0,2,5]],[false,true]],
            [5, [[0,1,10],[1,2,5],[2,3,9],[3,4,13]],  [[0,4,14],[1,4,13]],[true,false]],
           
        ]

    def distanceLimitedPathsExist(self, n: int, edgeList: List[List[int]], queries: List[List[int]]) -> List[bool]:
        g=[[None]*n for _ in range(n)]
        for f,t,v in edgeList:
            if g[f][t] is None or v<g[f][t]:
                g[t][f]=g[f][t]=v
        for g1 in g:
            self.log(g1)
        # @lru_cache(None)
        # mp=dict()
        def query(f,t,vt:set):
            if f==t:
                return 0
            # if (f,t)  in mp:
            #     return mp[f,t]
            vt.add(f)
            ret=inf
            for i in range(n):
                if g[f][i] is None or i in vt:
                    continue
                ret=min(ret,max(g[f][i],query(i,t,vt)))
            # mp[f,t]=mp[t,f]=ret
            self.log(f,t,ret)
            vt.remove(f)
            return ret


        return [query(f,t,set())<v for f,t,v in queries]


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



