from app.yly.algo.manage import SolutionBase,View
from collections import defaultdict
from typing import Dict,List
import math
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(nums = [1,1,1,1,1,1],result=6),
            dict(nums = [1,2,2,3,3,4],result=4),
        ]
    
    def subsequencesWithMiddleMode(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()
    
    def init(self, nums: List[int],**kw) -> int:
        self.nums=nums
        self.n = len(self.nums)
    def execute(self):
        suf=defaultdict(int)
        ans=math.comb(self.n,5)
        pre=defaultdict(int)
        for v in self.nums:
            suf[v]+=1
        for left,x in enumerate(self.nums[:-2]):
            suf[x]-=1
            if left>1:
                right = self.n-1-left
                pre_x,suf_x=pre[x],suf[x]
            pre[x]+=1



if __name__=='__main__':
    Solution().run()