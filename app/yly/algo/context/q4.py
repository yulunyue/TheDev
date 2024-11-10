

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
    uri = ""
    gameid = ''

    def get_cases(self):
        return [
            dict(num = "12355", t = 50,result="12355"),
            dict(num = "11111", t = 26,result="-1"),
            dict(num = "1234", t =256, result="1488")
        ]

    def execute(self):
        keys=[7,6,5,3,2]
        nums={}
        a={9:[3,2],8:[2,3],4:[2,2]}
        while self.t>1:
            ct=0
            for v in keys:
                if self.t%v!=0:
                    ct+=1
                    continue
                nums[v]=nums.get(v,0)+1
                self.t=self.t//v
            if ct==5:
                return "-1"
        def q(v):
            if v in a:
                return a[v]
            return v,1
        for v in self.num:
            if v==1:
                continue
            nm,t=q(v)
            if nm in nums:
                nums[nm]-=t
        self.log(nums)
        def check(n,a=None):
            self.log(n,nums,a)
            if all(v<=0 for v in nums.values()):
                return []
            
 
        for i in range(len(self.num)-1,0,-1):
            ni,ti=q(self.num[i])
            if ni in nums:
                nums[ni]+=ti
            for j in range(self.num[i],10):
                nj,tj=q(j)
                if nj in nums:
                    nums[nj]-=tj
                s1=check(len(self.num)-1-i,self.num[:i]+[j])
                if s1 is not None:
                    s2=self.num[:i]+[j]+s1
                    return "".join(str(v) for v in s2)
                if nj in nums:
                    nums[nj]+=tj
            if all(v<=0 for v in nums.values()):
                return self.num[:i]
                
                              
            

        


    def init(self, num: str, t: int) -> str:
        self.num,self.t=[int(v) for v in num],t

    def smallestNumber(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
