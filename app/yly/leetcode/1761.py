from sortedcontainers import SortedList
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
            [7, [[1, 3], [4, 1], [4, 3], [2, 5], [5, 6],
                 [6, 7], [7, 5], [2, 6], [7, 8]], 0],
            [6, [[1, 2], [1, 3], [3, 2], [4, 1], [5, 2], [3, 6]], 3]
        ]

    def minTrioDegree(self, n: int, edges: List[List[int]]) -> int:
        n += 2
        g = [[0]*n for _ in range(n)]
        ct = defaultdict(int)
        for f, t in edges:
            g[f][t] = 1
            g[t][f] = 1
            ct[f] += 1
            ct[t] += 1
        ret = inf
        for i in range(1, n):
            for j in range(i+1, n):
                if not g[i][j]:
                    continue
                for k in range(j+1, n):
                    if g[i][k] and g[j][k]:
                        ret = min(ret, ct[i]+ct[j]+ct[k]-6)
        return -1 if ret == inf else ret

    def test(self, *args):
        return self.minTrioDegree(*args)

    def check(self, *args):
        pass

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
