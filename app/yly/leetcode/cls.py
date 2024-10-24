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
    from app.yly.manage import SolutionBase
except:
    class SolutionBase:
        @classmethod
        def log(cls, *args, **kwargs):
            pass

        @classmethod
        def cls_run(cls):
            pass
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class Solution(SolutionBase):
    @classmethod
    def get_cases(cls):
        return [

        ]


if __name__ == '__main__':
    Solution().cls_run()
