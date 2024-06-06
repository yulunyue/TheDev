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
'''
1,4,3,
7
4,5

'''

class Solution:
    def get_cases(self):
        return [
            [[1,4,3,7,4,5], 3,15],
        ]
    
    def maximumScore(self, nums: List[int], k: int) -> int:
        n=len(nums)
        ln,rn=[],[]
        left_min=right_min=nums[k]
        l,r=k-1,k+1
        while l>=0:
            if nums[l]<=left_min:
                ln.append([k-l-1,left_min])
                left_min=nums[l]
            l-=1
        ln.append([k-l-1,left_min])
        while r<n:
            if nums[r]<=right_min:
                rn.append([r-k-1,right_min])
                right_min=nums[r]
            r+=1
        rn.append([r-k-1,right_min])
        self.log(ln)
        self.log(rn)
        
    def check(self,*args):
        pass
    
    def test(self,*args):
        return self.maximumScore(*args)

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



