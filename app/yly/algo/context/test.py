

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
        mv=0
        idx=0
        l2,l3=[],[]
        def l_append(q:List[int],i1,i2):
            tmp=[]
            if self.nums[i1]!=-1:
                tmp.append(self.nums[i1])
            if i2<len(self.nums) and self.nums[i2]!=-1:
                if tmp and tmp[0]>self.nums[i2]:
                    tmp.insert(0,self.nums[i2])
                else:
                    tmp.append(self.nums[i2])
            q.append(tmp)
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
        def checkl(v,l,n):
            for a in l:
                pass
        def check(c):
            self.x1=self.x2=mv
            self.y1=self.y2=max_r
            if l2 and not checkl(c,l2,2):
                return False
            if l3 and not checkl(c,l3,3):
                return False
            return True

        ans=l=mv
        r=max_r
        while l<=r:
            m=(l+r)//2
            if check(m):
                ans=m
                l=m+1
            else:
                r=m-1
        # l2.sort()
        # l3.sort()
        self.log(l2,l3,mv)
        # if len(l2)==1 and len(l3)==1:
        #     return 0
        # if len(l2)>=1:
        #     mv=max(mv,math.ceil((l2[-1]-l2[0])/2))
        # if len(l3)>=1:
        #     mv=max(mv,math.ceil((l3[-1]-l3[0])/3))
       
        return ans


  
        
    def minDifference(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
