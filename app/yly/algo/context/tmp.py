from app.yly.algo.manage import SolutionBase
from typing import Dict,List
import heapq
from functools import lru_cache
import math
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(nums =[66307295,441787703,589039035,322281864],k =900900704,multiplier=641725,result=0),
            dict(nums =[5,1],k =2,multiplier =3,result=[5,9]),
            dict(nums =[1],k =3,multiplier =10,result=[1000]),
            dict(nums = [2,1,3,5,6], k = 5, multiplier = 2,result=[8,4,6,5,6])
        ]
    

    def init(self, nums: List[int], k: int, multiplier: int,**kw) -> List[int]:
        self.result = nums[:]
        self.max_num=max(nums)
        self.nums =[[v,i] for i,v in  enumerate(nums)]
        self.k=k
        self.multiplier = multiplier
    
    def execute(self):
        if self.multiplier == 1:
            return self.result
        if len(self.result)==1:
            return [self.result[0]*pow(self.multiplier,self.k,MOD)%MOD]
        heapq.heapify(self.nums)
        while self.k>0 and self.nums[0][0]<self.max_num:
            v,i=self.nums[0]
            heapq.heapreplace(self.nums,[v*self.multiplier,i])
            self.k-=1
        n=len(self.nums)
        self.nums.sort()
        for i in range(n):
            v,j=self.nums[i]
            pk=self.k//n+(i<self.k%n)
            self.result[j]= v*pow(self.multiplier,pk,MOD)%MOD
        return self.result

    
    def getFinalState(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()

if __name__=='__main__':
    Solution().run()