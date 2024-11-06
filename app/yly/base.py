

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

    def init(self):
        pass

    def execute(self):
        pass

    def xx(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute


if __name__ == '__main__':
    Solution().run()
