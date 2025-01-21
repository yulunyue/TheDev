from app.yly.algo.manage import SolutionBase,View,np
from typing import Dict,List
from functools import lru_cache
import heapq
from collections import defaultdict
import bisect
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(nums = [1,2,3], k = 2,result=20),
            dict(nums = [1,-3,1], k = 2,result=-6),
        ]
    
    def minMaxSubarraySum(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()
    
    def init(self, nums: List[int], k: int) -> int: 
        self.nums=nums
        self.k=k
    
    def execute(self):
        def calc_min(nums):
            q=[]
            for i,v in enumerate(nums):
                heapq.heappush(q,[v,i])
                while q and q[0][1]<=i-self.k:
                    v,j=heapq.heappop(q)
                    self.log('pop',j,v)
                self.log(q)
        a=calc_min(self.nums)
        #b=calc_min([-v for v in self.nums])
        return a



if __name__=='__main__':
    Solution().run()