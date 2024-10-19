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
            dict(nums=[4, 1], cost1=5, cost2=2, result=15)
        ]

    def execute(self, nums: List[int], cost1: int, cost2: int) -> int:
        n = len(nums)
        max_num, min_num = max(nums), min(nums)
        nums = [max_num-v for v in nums if v != max_num]
        sum_num = sum(nums)
        if n <= 2 or cost1*2 <= cost2:
            return sum_num*cost1 % M

        def f(x):
            pass

        @lru_cache(None)
        def dfs(i, v):
            if i < 0:
                return v
            ans = dfs(i-1, v)
            dfs(i-1, v-nums[i])

        min_value = dfs(len(nums)-1, sum_num/2)

    def minCostToEqualizeArray(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
