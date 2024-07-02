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
            [[1,2,3], [6,5],0]
        ]
    
    def getXORSum(self, arr1: List[int], arr2: List[int]) -> int:
        N=36
        def ct(arr):
            ret=[0]*N
            for a in arr:
                i=0
                while a>0:
                    if a%2==1:
                        ret[i]+=1
                    a=a//2
                    i+=1
            return ret
        arr1=ct(arr1)
        arr2=ct(arr2)
        ret=0
        for i in range(N):
            if (arr1[i]*arr2[i])%2==1:
                ret+=1<<i
        self.log(arr1,arr2)
        return ret
    def check(self,*args):
        pass
    
    def test(self,*args):
        return self.getXORSum(*args)

    def init(self,*args):
        pass

    def __init__(self,*args) -> None:
        self.local_debug=getattr(self,sys.argv[-1],None)
        self.init(*args)
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



