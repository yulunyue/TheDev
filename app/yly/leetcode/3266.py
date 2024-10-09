from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
try:
    from app.yly.leetcode.manage import SolutionBase
except:
    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def run(self):
            pass
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(nums = [2,1,3,5,6], k = 5, multiplier = 2,result=[8,4,6,5,6])
        ]


    def execute(self, nums: List[int], k: int, multiplier: int) -> List[int]:
        n=len(nums)
        num2=sorted([[v,i] for i,v in enumerate(nums)])
        min_num=num2[0][0]
        num3=[0]*n
        self.log(num2)
        while k>0:
            min_num*=multiplier
            l=bisect.bisect_right(num2,[min_num,inf])
            for i in range(min(l,k)):
                num3[num2[i][1]]+=1
            k-=l
            # self.log(k,min_num,l,num3)
        return [(v*pow(multiplier,num3[i],M))%M for i,v in enumerate(nums)]
            

    def getFinalState(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
