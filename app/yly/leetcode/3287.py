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
            dict(nums = [4,2,5,6,7], k = 2,result=2)
        ]


    def execute(self, nums: List[int], k: int) -> int:
        n=len(nums)-k-1
        def dfs(num):
            ret=[0]*n
            for i in range(k):
                for j in range(n):
                    ret[j]|=num[i+j]
            res=[{ret[i]} for i in range(n)]
            for j in range(1,n):
                for v in res[j-1]:
                    res[j].add(v|num[j])
            return res
        num1=dfs(nums)
        num2=dfs(nums[::-1])
        self.log(num1,num2)
        ans=0
        for a in num1:
            for b in num2:
                for c in a:
                    for d in b:
                        ans=max(ans,c^d)
                        self.log(c,d,c^d,ans)
        return ans
    def maxValue(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
