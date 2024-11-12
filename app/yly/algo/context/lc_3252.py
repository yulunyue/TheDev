

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

        def run(self):
            pass

        def watch(self):
            pass


class Solution(SolutionBase):
    uri = "https://leetcode.cn/problems/count-k-reducible-numbers-less-than-n/"
    gameid = ''

    def get_cases(self):
        return [
            dict(s="1000", k=2, result=6),  # 1 2 3 4 5 6
            dict(s="111", k=1, result=3),
        ]

    def execute(self):
        n = len(self.s)

        @lru_cache(None)
        def dfs(i, j, limit=True):
            pass
        return dfs(0, self.k)

    def init(self, s: str, k: int) -> int:
        self.s = s
        self.k = k

    def countKReducibleNumbers(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
