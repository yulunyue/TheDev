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
    from app.yly.algo.manage import SolutionBase
except:
    class SolutionBase:
        pass
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(array=[7, 1, 3, 2, 5, 4, 6], result=[1, 2, 3, 4, 5, 6, 7])
        ]

    def execute(self, array: List[int], result=None):
        RECORD_ENABLE = True
        n = len(array)
        for i in range(n):
            for j in range(i):
                if array[i] > array[j]:
                    array[i], array[j] = array[j], array[i]
        return array

    def sort(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
