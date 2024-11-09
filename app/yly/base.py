

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
    uri = ""
    gameid = ''

    def get_cases(self):
        return [

        ]

    def execute(self):
        pass

    def xx(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
