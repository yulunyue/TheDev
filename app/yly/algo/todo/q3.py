from app.yly.algo.manage import SolutionBase,View
from typing import Dict,List
from functools import lru_cache
from collections import defaultdict
from common.algo.math_util import gcd
import bisect
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            # dict(nums = range(1,1000),result=3),
            dict(nums = [3,4,3,4,3,4,3,4],result=3.1)
        ]
    
    def numberOfSubsequences(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()
        
    def init(self, nums: List[int]) -> int:
        self.nums=nums

    def execute(self):
        '''
        p*r=q*s
        p/q=s/r
        '''
        n=len(self.nums)
        cnt=defaultdict(int)
        ans=0
        for r in range(3,n):
            q=r-2
            for p in range(0,q-1):
                g=gcd(self.nums[p],self.nums[q])
                cnt[self.nums[q]//g,self.nums[p]//g]+=1
            for s in range(r+2,n):
                g=gcd(self.nums[r],self.nums[s])
                ans+= cnt[self.nums[r]//g,self.nums[s]//g]
        return ans

if __name__=='__main__':
    Solution().run()