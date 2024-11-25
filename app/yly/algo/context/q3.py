

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import os
import heapq
inf = float("inf")
MOD = (10**9)+7
try:
    from app.yly.algo.manage import SolutionBase,U
except Exception as e:
    print(e,file=sys.stderr)
    class U:
        @staticmethod
        def fmax(a,b,*args):return a if a>b else b
        @staticmethod
        def fmin(a,b,*args):return a if a<b else b
        @staticmethod
        def get_info(*args):
            pass
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


class Solution(SolutionBase):
    uri = "https://leetcode.cn/contest/weekly-contest-425/problems/minimum-array-sum/description/"
    gameid = ''

    def get_cases(self):
        return [
            dict(nums = [882,307,624,469,329,684,851,608,317,205],k =431,op1 =9,op2=4,result=1582.1),
            dict(nums=[0,4],k=3,op1=1,op2=1,result=1),
            dict(nums = [2,8,3,19,3], k = 3, op1 = 1, op2 = 1,result=23),
            
            
            dict(nums =[10],k =3,op1 =1,op2 =1,result=2),
            dict(nums =[9],k =5,op1 =1,op2 =1,result=0),
           
            
        ]

    def execute_tanxin(self, nums: List[int], k: int, op1: int, op2: int) -> int:
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
    
    def execute(self, nums: List[int], k: int, op1: int, op2: int) -> int:
        #nums.sort()

        @lru_cache(None)
        def dfs(n,op1,op2):
            if op1==0 and op2==0:
                return 0
            if n<0:
                return 0
            ans=dfs(n-1,op1,op2)
            if op1>0:
                ans=U.fmax(ans,nums[n]//2+dfs(n-1,op1-1,op2),n,f'op1 {nums[n]}')
            if op2>0 and nums[n]>=k:
                ans=U.fmax(ans,k+dfs(n-1,op1,op2-1), n,f'op2 {nums[n]}')
            if op1>0 and op2>0:
                if nums[n]>=2*k-1:
                    ans=U.fmax(ans,k+nums[n]//2+dfs(n-1,op1-1,op2-1),n,f'op1 op2 {nums[n]}')
                elif nums[n]>=k:
                    ans=U.fmax(ans,nums[n]-(nums[n]-k+1)//2+dfs(n-1,op1-1,op2-1),n,f'op2 op1 {nums[n]}')
            return ans
        ans=dfs(len(nums)-1,op1,op2)
        self.log(U.get_info(len(nums)-1,ans))
        return sum(nums)-ans

    def minArraySum(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute(*arg, **kg)


if __name__ == '__main__':
    Solution().run()
