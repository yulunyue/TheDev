from app.yly.algo.manage import SolutionBase,View
from typing import Dict,List
from functools import lru_cache
from collections import defaultdict
import bisect
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    uri="https://leetcode.cn/problems/minimum-increments-for-target-multiples-in-an-array/description/"
    def get_cases(self):
        return [
            dict(nums =[8,10,9],
target =[10,6,6],result=3),
            dict(nums = [8,4], target = [10,5],result=2),
            dict(nums = [1,2,3], target = [4],result=1),
        ]
    def minimumIncrements(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
    def execute(self, nums: List[int], target: List[int]) -> int:

        nums.sort()
        mask=(2**len(target))-1
        mx=[[] for _ in target]
        for i,v in enumerate(target):
            while v<nums[-1]+target[i]:
                mx[i].append(v)
                v+=target[i]
        inf=float("inf")
        f=[inf]*(mask+1)
        f[0]=0
        self.log(mx)
        for v in nums:
            for i in range(len(target)):
                s=2**i
                while mx[i][0]<v:
                    mx[i].pop(0)
                for m in range(mask,-1,-1):
                    if m&s==0:
                        f[m|s]=min(f[m|s],f[m]+mx[i][0]-v)
                self.log(v,i,f)
        self.log(f)
        return f[mask]



if __name__=='__main__':
    Solution().run()