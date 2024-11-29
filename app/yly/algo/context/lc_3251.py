

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
    from app.yly.algo.manage import SolutionBase,div,bp,divh,divv

except:
    def fmax(a,b,*args):return a if a>b else b
    def fmin(a,b,*args):return a if a<b else b
    class SolutionBase:
        DEV = False

        def log(self, *args, **kwargs):
            pass
        def init(self,*args,**kwargs):
            pass
        def execute(self, *args, **kwargs):
            pass

        def exec(self):
            pass

        def run(self):
            print(self.exec())

  


class Solution(SolutionBase):
    uri = ""
    gameid = ''
    name = ''
    tags = []
    has_view = False
    def get_cases(self):
        return [
            dict(nums = [2,3,2],result=4),
            dict(nums = [5,5,5,5],result=126),
        ]
    
    def execute(self, nums: List[int]) -> int:
        m=(10**9)+7
        n=len(nums)
        @lru_cache(None)
        def dfs(i,a,b):
            if i==n:
                return 1
            ans=0
            a=max(a,nums[i]-b)
            for v in range(a,nums[i]+1):
                ans+=dfs(i+1,v,nums[i]-v)
            return ans
        return dfs(0,0,nums[0])%m
    
    def execute(self, nums: List[int]) -> int:
        n=len(nums)

        dp=[[1 if i==0 else 0]*nums[i] for i in range(n)]
        for i in range(1,n):
            dp[i][0]=1
            for j in range(len(dp[i])):
                for k in range(j):
                    dp[i][j]=(dp[i][j]+dp[i-1][k])%MOD
        self.log(dp)
        return sum(dp[-1])%MOD

    def countOfPairs(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute(*arg, **kg)


if __name__ == '__main__':
    Solution().run()
