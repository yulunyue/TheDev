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
    from app.yly.leetcode.manage import SolutionBase
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

MAX_N = 10**5


def prime_flags(max_v):
    ret = [None]*max_v
    for i in range(2, max_v):
        if ret[i] == False:
            continue
        ret[i] = True
        for j in range(i+i, max_v, i):
            ret[j] = False
    return ret


ZHI_SHU = prime_flags(MAX_N+1)


class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(n=5,
                 edges=[[1, 5], [2, 1], [4, 5], [3, 2]],
                 result=4),
            dict(n=5, edges=[[1, 2], [1, 3], [2, 4], [2, 5]], result=4)
        ]

    def execute(self, n: int, edges: List[List[int]]) -> int:
        g = defaultdict(list)
        for f, t in edges:
            g[f].append(t)
            g[t].append(f)
        self.ans = 0

        def dfs(cid, pid):
            one_cnt = 1 if ZHI_SHU[cid] else 0
            zero_cnt = 1 - one_cnt
            for nid in g[cid]:
                if nid == pid:
                    continue
                none_cnt, nzero_cnt = dfs(nid, cid)
                if ZHI_SHU[cid]:
                    self.ans += zero_cnt * nzero_cnt
                else:
                    self.ans += one_cnt * nzero_cnt+zero_cnt*none_cnt
                zero_cnt += nzero_cnt
                one_cnt += none_cnt
            self.log(cid, one_cnt, zero_cnt, self.ans)
            return one_cnt, zero_cnt
        dfs(1, 0)
        return self.ans

    def countPaths(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
