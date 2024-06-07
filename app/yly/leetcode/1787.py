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
            [[1,2,3,1,2,3,4],3,0.1],
            [[1,2,4,1,2,5,1,2,6], 3,3],
            [[1,2,0,3,0], 1,3],
            [[23,27,14,0,14,3,7,10,14,23,5,5],1,11],
        ]
    def minChanges(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if k==1:
            return len([v for v in nums if v])
        ct=[defaultdict(int)  for _ in range(k)]
        max_ct=[0]*k
        for i,v in enumerate(nums):
            ct[i%k][v]+=1
            max_ct[i%k]=max(max_ct[i%k],ct[i%k][v])
        ans = sum(sorted(max_ct)[-k+1:])
        self.log(n,ans,ct)
        @lru_cache(None)
        def dfs(i,s):
            if i>=k:
                return 0 if s==0 else -inf
            ret=-inf
            for j,v in ct[i].items():
                ret=max(
                    ret,
                    v+dfs(i+1,s+j),
                    v+dfs(i+1,s-j)
                )
            return ret
        ans=max(ans,dfs(0,0))
        return n-ans


    def check(self,*args):
        pass
    
    def test(self,*args):
        return self.minChanges(*args)

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



