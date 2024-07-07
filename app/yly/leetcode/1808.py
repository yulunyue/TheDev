from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class Solution:
    def get_cases(self):
        return [
            [5, 6],
            [8, 18],
        ]

    def check(self, *args):
        pass

    def maxNiceDivisors(self, primeFactors: int) -> int:
        @lru_cache(None)
        def dfs(n):
            if n <= 3:
                return n-1
            if n == 4:
                return 3
            ret = 2
            for i in range(2, n-2):
                ret = max(ret, i*dfs(n-i)) % M
            self.log(n, ret)
            return ret
        return dfs(primeFactors)

    def test(self, *args):
        return self.maxNiceDivisors(*args)

    def __init__(self) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s):
        if not self.local_debug or len(self.logs) >= 2048:
            return
        self.logs += " ".join([str(v) for v in s])+"\n"

    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs = ""
            try:
                r = self.local_debug(*case[:-1])
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, case[-1]):
                self.check(*case, r)
                print(case, r)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
