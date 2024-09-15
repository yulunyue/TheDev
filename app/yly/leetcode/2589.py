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
            dict(tasks=[[1, 3, 2], [2, 5, 3], [5, 6, 2]], result=4),
            dict(tasks=[[2, 3, 1], [4, 5, 1], [1, 5, 2]], result=2)
        ]

    def execute(self, tasks: List[List[int]]) -> int:
        RECORD_ENABLE = True
        n = len(tasks)
        tasks.sort()
        q = []
        for i in range(n):
            s, t, d = tasks[i]
            if q and q[-1][1] >= s:
                q[-1][2] = max(q[-1][2], d)
                q[-1][1] = t
                continue
            q.append([s, t, d])
        self.log(q)

    def findMinimumTime(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
