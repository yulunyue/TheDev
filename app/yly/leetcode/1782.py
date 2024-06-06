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


class Solution:
    def get_cases(self):
        return [
            [5, [[1,5],[1,5],[3,4],[2,5],[1,3],[5,1],[2,3],[2,5]],[1,2,3,4,5],[10,10,9,8,6]],
            [4, [[1,2],[2,4],[1,3],[2,3],[2,1]], [2,3],[6,5]]
        ]


    def check(self,*args):
        pass

    def countPairs(self, n: int, edges: List[List[int]], queries: List[int]) -> List[int]:
        n=len(edges)
        cont_e=defaultdict(int)
        ct_n=[0]*(len(edges)+1)
        for e1,e2 in edges:
            if e1>e2:
                e1,e2=e2,e1
            self.log(e1,e2)
            cont_e[e1]+=1
            cont_e[e2]+=1
            cont_e[e1,e2]+=1
        for i in range(1,n):
            for j in range(i+1,n):
                c=cont_e[i]+cont_e[j]-cont_e[i,j]
                self.log(i,j,c)
                ct_n[c]+=1
        ct_n1=list(accumulate(ct_n))
        # self.log(ct_n,ct_n1)
        ret=[]
        for q in queries:
            ret.append(ct_n1[-1]-ct_n1[q])
        return ret

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



