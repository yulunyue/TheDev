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
            [[231,167,89,85,224,180,45,58,23,108,157,95,108,64,206,109,147,28,194,17,4,46,74,96,237,109,114,122,161,76,181,251,9,82,44,15,242,7,23,109,210,109,181,12,14,226,61,49,8,74,19,152,4,137,243,27,187,200,168,145,188,203,98,193,253,133,164,198,132,119,148,146,94,43,181,123,212,83,157],2,75],
            [[1,2,3,1,2,3,4],3,1],
            [[1,2,4,1,2,5,1,2,6], 3,3],
            [[1,2,0,3,0], 1,3],
            [[23,27,14,0,14,3,7,10,14,23,5,5],1,11],
        ]
    def minChanges(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if k==1:
            return len([v for v in nums if v])
        ct=[defaultdict(int)  for _ in range(k)]
        for i,v in enumerate(nums):
            ct[i%k][v]+=1
        ans=[]
        for i in range(k):
            ans.append(max(ct[i].values()))
        ret = n-sum(ans)
        @lru_cache(None)
        def dfs(i,s):
            if i==k:
                return 0 if s==0 else inf
            r=0
            for j,v in ct[i].items():
                r=min(r,dfs(i+1,s^j)-v)
            return ans[i]+r
        
        return ret+dfs(0,0)


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



