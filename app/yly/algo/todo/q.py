from app.yly.algo.manage import SolutionBase,View
from typing import Dict,List
from collections import defaultdict
from sortedcontainers import SortedList
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(nums = [-3,2,-2,-1,3,-2,3],result=7)
        ]
    def init(self, nums: List[int]) -> int:
        self.nums=nums

    def maxSubarraySum(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()
        
    def execute(self):
      
        tmp_sum1=0
        tmp_sum2=0
        ans=max(self.nums)
        ct=defaultdict(int)
        l=0
        min_ct = SortedList()
        for i,v in enumerate(self.nums):
            if v>=0:
                tmp_sum1+=v
            else:
                tmp_sum2+=v
                if ct[v]:
                    min_ct.remove(ct[v])
                ct[v]-=v
                min_ct.add(ct[v])
            while l<=i and tmp_sum1+tmp_sum2+(min_ct[-1] if min_ct else 0)<0:
                u=self.nums[l]
                if u>=0:
                    tmp_sum1-=u
                else:
                    tmp_sum2-=u
                    min_ct.remove(ct[u])
                    ct[u]+=u
                    if ct[u]:
                        min_ct.add(ct[u])
                    # ans=max(ans,tmp_sum1+min_ct[-1])
                l+=1
            ans=max(ans,tmp_sum1+tmp_sum2+(min_ct[-1] if min_ct else 0))
            self.log(ans,tmp_sum1,tmp_sum2,list(min_ct),self.nums[l:i+1])
     
            
        return ans



if __name__=='__main__':
    Solution().run()