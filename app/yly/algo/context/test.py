

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
MOD = (10**9)+7
try:
    from app.yly.algo.manage import SolutionBase

except:

    class SolutionBase:
        DEV = False

        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass
        def exec(self):
            pass
        def run(self):
            print(self.exec())

        def watch(self):
            pass


class Solution(SolutionBase):
    uri = "https://leetcode.cn/problems/minimize-the-maximum-adjacent-element-difference/"
    gameid = ''

    def get_cases(self):
        return [
            dict(nums=[20,-1,72,-1,108],result=26),
            dict(nums=[1,12],result=11),
            dict(nums=[-1,-1,-1,38],result=0),
            dict(nums=[14,-1,-1,46],result=11),
            dict(nums = [1,2,-1,10,8],result=4),
            dict(nums=[-1,-1,-1],result=0),       
        ]


    def init(self, nums: List[int]) -> int:
        self.nums=nums
    
    def execute(self):
        n = len(self.nums)
        min_v,max_v=inf,0

        max_r=0
        while idx<n:
            max_r=max(max_r,self.nums[idx])
            i=idx+1
            while i<n and self.nums[i]==-1:
                i+=1
            if i==idx+2:
                l_append(l2,idx,i)
            elif i>idx+2:
                l_append(l3,idx,i)
            elif i<n and i>0 and self.nums[i-1]!=-1:
                mv=max(mv,abs(self.nums[i]-self.nums[i-1]))
            idx=i

       
        return ans


  
        
    def minDifference(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
