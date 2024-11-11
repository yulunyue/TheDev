

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
    from app.yly.manage import SolutionBase

except:

    class SolutionBase:
        DEV = False

        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            pass

        def watch(self):
            pass


class Solution(SolutionBase):
    uri = "https://leetcode.cn/problems/maximum-frequency-of-an-element-after-performing-operations-ii/"
    gameid = ''

    def get_cases(self):
        return [
            dict(nums =[5,64],k =42,numOperations=2,result=2),
            dict(nums =[1,2,4,5],k =2,numOperations =4,result=4),
            dict(nums =[94,10,92],k =0,numOperations =3,result=1),
            dict(nums = [5,11,20,20], k = 5, numOperations = 1,result=2),
            dict(nums = [1,4,5], k = 1, numOperations = 2,result=2),
        ]

    def execute(self):
        a,b=min(self.nums),max(self.nums)
        n=b-a+1
        ct=[0]*n
        for v in self.nums:
            ct[v-a]+=1
        for i in range(1,n):
            ct[i]+=ct[i-1]
        ans=1
        self.log(ct)
        for i in range(1,n):
            tmp=ct[i]-ct[i-1]
            if tmp+self.numOperations<=ans:
                continue
            l=i-self.k-1
            if l<0:
                l=0
            r=i+self.k
            if r>=n:
                r=n-1
            lc = ct[i-1]-ct[l]+ct[r]-ct[i]
            if lc>self.numOperations:
                lc=self.numOperations
            if tmp+lc>ans:
                ans=tmp+lc
            self.log(i,tmp,ct[i-1]-ct[l],ct[r]-ct[i],ans)
        return ans

    def init(self, nums: List[int], k: int, numOperations: int) -> int:
        self.nums,self.k,self.numOperations=nums,k,numOperations
    def maxFrequency(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
