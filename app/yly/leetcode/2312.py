from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
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
            dict(m=3, n=5, prices=[[1, 4, 2], [2, 2, 7], [2, 1, 3]], result=19)
        ]

    def xx(self, m, n, prices):
        ct = defaultdict(dict)
        for y, x, p in prices:
            ct[y][x] = p

        @lru_cache(None)
        def dfs_col(i, j):
            ret = 0
            for k, v in ct[i].items():
                if k <= j:
                    ret = max(ret, v+dfs_col(i, j-k))
            # self.log('col', i, j, ret)
            return ret

        @lru_cache(None)
        def dfs_row(i):
            ret = 0
            for k in ct.keys():
                if k <= i:
                    ret = max(ret, dfs_col(k, n)+dfs_row(i-k))
            # self.log('row', i, ret)
            return ret

        return dfs_row(m)

    def test(self, **kg):
        return self.xx(**kg)

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s, tp: str = ""):
        if not self.local_debug or len(self.logs) >= 102400:
            return
        if tp:
            self.draw(s[0], tp)
        self.logs += " ".join([str(v) for v in s])+"\n"

    def draw(self, s, tp: str):
        from common.tool.draw import Draw
        d = Draw()
        if tp.startswith('bar'):
            d.draw_bar_chart(s)
        elif tp.startswith('graph'):
            d.draw_graph(s)
        d.save(f"data/log/{tp}.png")

    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs = ""
            self.ep = case.pop("result")
            try:
                r = self.local_debug(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, self.ep):
                print(case, 'result', r, 'except', self.ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
