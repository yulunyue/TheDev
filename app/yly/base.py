

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
try:
    from app.yly.manage import SolutionBase

except:
    class SolutionBase:
        def input(self):
            return input()

        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            pass


class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/tic-tac-toe"
    gameid = ''

    def get_cases(self):
        return [

        ]

    def execute(self):
        pass


if __name__ == '__main__':
    Solution().run()
