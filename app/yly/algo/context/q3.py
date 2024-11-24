

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
        def init(self,*args,**kwagrs):
            pass
        def execute(self, *args, **kwargs):
            pass
        def exec(self):
            pass
        def run(self):
            print(self.exec())

        def watch(self):
            pass
fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Solution(SolutionBase):
    uri = "https://leetcode.cn/contest/weekly-contest-425/problems/minimum-array-sum/description/"
    gameid = ''

    def get_cases(self):
        return [
            dict(nums=[0,4],k=3,op1=1,op2=1,result=1),
            dict(nums = [2,8,3,19,3], k = 3, op1 = 1, op2 = 1,result=23),
            dict(nums = [882,307,624,469,329,684,851,608,317,205],k =431,op1 =9,op2=4,result=1582),
            
            dict(nums =[10],k =3,op1 =1,op2 =1,result=2),
            dict(nums =[9],k =5,op1 =1,op2 =1,result=0),
           
            
        ]

    def execute(self, nums: List[int], k: int, op1: int, op2: int) -> int:
        sall=sum(nums)
        nums=sorted(nums)
        self.log(nums)
        ans=0
        n=len(nums)
        ki2=bisect.bisect_left(nums,2*k-1)
        ki=bisect.bisect_left(nums,k)
        for i in range(n-1,ki2-1,-1):
            c=nums[i]
            if op1<=0 and op2<=0:
                break
            if op1>0:
                self.log(1,i,nums[i])
                c=(c+1)//2
                op1-=1
            if op2>0:
                c-=k
                self.log(2,i,nums[i])
                op2-=1
            ans+=nums[i]-c
        # ki+=1
        while op2>0 and ki<ki2:
            self.log(2,ki,nums[ki])
            nums[ki]-=k
            ans+=k
            op2-=1
            ki+=1
        nums=sorted(nums[:ki2])
        self.log(nums)
        while op1>0 and nums:
            self.log(1,len(nums)-1,nums[-1])
            ans+=nums.pop()//2
            op1-=1
        self.log(ans)
        return sall-ans
    
    def execute2(self, nums: List[int], k: int, op1: int, op2: int) -> int:
        nums.sort()
        @lru_cache(None)
        def dfs(n,op1,op2):
            if op1==0 and op2==0:
                return 0
            if n<0:
                return 0
            ans=dfs(n-1,op1,op2)
            if op1>0:
                ans=max(ans,nums[n]//2+dfs(n-1,op1-1,op2))
            if op2>0 and nums[n]>=k:
                ans=max(ans,k+dfs(n-1,op1,op2-1))
            if op1>0 and op2>0:
                if nums[n]>=2*k-1:
                    ans=max(ans,k+nums[n]//2+dfs(n-1,op1-1,op2-1))
                elif nums[n]>=k:
                    ans=max(ans,nums[n]-(nums[n]-k+1)//2+dfs(n-1,op1-1,op2-1))
            self.log(nums[:n+1],op1,op2,ans)
            return ans
        
        return sum(nums)-dfs(len(nums)-1,op1,op2)
    
    def execute2(self, nums: List[int], k: int, op1: int, op2: int) -> int:
        def f(x): return x - x // 2
        def g(x): return x if x < k else x - k
        dp = [[0] * (op2 + 1) for _ in range(op1 + 1)]
        dp[0][0] = 0
        for v in nums:
            v1 = v // 2
            v2 = 0 if v < k else k
            v12 = v - fmin(f(g(v)), g(f(v)))
            for i in range(op1, -1, -1):
                for j in range(op2, -1, -1):
                    if i: dp[i][j] = fmax(dp[i][j], dp[i - 1][j] + v1)
                    if j: dp[i][j] = fmax(dp[i][j], dp[i][j - 1] + v2)
                    if i and j:
                        dp[i][j] = fmax(dp[i][j], dp[i - 1][j - 1] + v12)
        return sum(nums) - dp[-1][-1]
    def minArraySum(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute(*arg, **kg)


if __name__ == '__main__':
    Solution().run()
