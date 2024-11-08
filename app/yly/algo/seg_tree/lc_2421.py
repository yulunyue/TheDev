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
            dict(vals=[1, 3, 2, 1, 3], edges=[
                 [0, 1], [0, 2], [2, 3], [2, 4]], result=6)
        ]

    def execute(self, vals: List[int], edges: List[List[int]]):
        RECORD_ENABLE = True
        n = len(vals)
        g = [[] for _ in range(n)]
        for f, t in edges:
            g[f].append(t)
            g[t].append(f)
        fa = list(range(n))
        size = [1]*n

        def find(x):
            if x != fa[x]:
                fa[x] = find(fa[x])
            return fa[x]
        ans = n
        values = sorted([[v, i] for i, v in enumerate(vals)])
        for v, pid in values:
            ppid = find(pid)
            for pnid in g[pid]:
                pnid = find(pnid)
                if vals[pnid] > v or pnid == ppid:
                    continue
                if vals[pnid] == v:
                    ans += size[ppid]*size[pnid]
                    size[ppid] += size[pnid]
                fa[pnid] = ppid
        return ans

    def numberOfGoodPaths(self, *args, **kg) -> int:
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
