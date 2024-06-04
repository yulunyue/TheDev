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
            [[9,16,30,23,33,35,9,47,39,46,16,38,5,49,21,44,17,1,6,37,49,15,23,46,38,9,27,3,24,1,14,17,12,23,43,38,12,4,8,17,11,18,26,22,49,14,9],[[17,0],[30,17],[41,30],[10,30],[13,10],[7,13],[6,7],[45,10],[2,10],[14,2],[40,14],[28,40],[29,40],[8,29],[15,29],[26,15],[23,40],[19,23],[34,19],[18,23],[42,18],[5,42],[32,5],[16,32],[35,14],[25,35],[43,25],[3,43],[36,25],[38,36],[27,38],[24,36],[31,24],[11,31],[39,24],[12,39],[20,12],[22,12],[21,39],[1,21],[33,1],[37,1],[44,37],[9,44],[46,2],[4,46]],[-1,21,17,43,10,42,7,13,29,44,17,31,39,10,10,29,32,0,40,23,12,39,12,40,25,35,15,38,40,40,17,24,5,1,19,14,17,21,25,24,14,17,40,25,37,17,10]],
            [[2,3,3,2], [[0,1],[1,2],[1,3]],[-1,0,0,1]],
        ]

    def getCoprimes(self, nums: List[int], edges: List[List[int]]) -> List[int]:
        n=len(nums)
        p=[None]*n
        max_v=51
        state=[0]*max_v
        idx=0
        for i in range(2,max_v):
            if state[i]!=0:
                continue
            j=1
            while i*j<max_v:
                state[i*j]|=1<<idx
                j+=1
            idx+=1
       
        # self.log(state)
        for f,t in edges:
            p[t]=f
        self.log(p)
        ret=[]
        # @lru_cache(None)
        def dfs(n):
            s=state[nums[n]]
            # self.log('dfs',n,nums[n],s)
            if p[n] is None:
                return -1
            n=p[n]
            while state[nums[n]]&s!=0:
                if p[n] is None:
                    return -1
                n=p[n]
                # self.log(n,nums[n],state[nums[n]])
            return n


        for i in range(n):
            ret.append(dfs(i))
        return ret
        
    def check(self,*args):
        pass

    def __init__(self) -> None:
        self.local_debug=getattr(self,sys.argv[-1],None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")

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



