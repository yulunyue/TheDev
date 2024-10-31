

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
    DEV = True
except:
    DEV = False

    class SolutionBase:
        @staticmethod
        def get_info(self, **kw):
            return dict()

        def input(self):
            return input()

        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            pass


class Solution(SolutionBase):
    uri = ""
    gameid = ''

    def get_cases(self):
        return [

        ]

    def execute(self, *args, **kw):
        return self.xx(*args, **kw)


if __name__ == '__main__':
    Solution().run()
