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
            dict(num1="1",
                 num2="5",
                 min_num=1,
                 max_num=5,
                 result=5),
            dict(num1="1", num2="12", min_num=1, max_num=8, result=11),
        ]

    def count(self, num1: str, num2: str, min_num: int, max_num: int) -> int:
        num1 = num1.zfill(len(num2))

        @lru_cache(None)
        def dfs(i, n, up_limit=True, down_limit=True):
            if i == len(num1):
                return 1
            if n < 0:
                return 0
            ret = 0
            if up_limit:
                r = int(num2[i])+1
                l = min(int(num1[i]), int(num2[i])) if down_limit else 0
            else:
                l, r = 0, 10
            for v in range(l, r):
                if v > n:
                    continue
                next_up_limit = up_limit if v == r-1 else False
                next_down_limit = down_limit and not up_limit
                ret += dfs(i+1, n-v, next_up_limit, next_down_limit)
            self.log(i, n, l, r, up_limit, down_limit, ret)
            return ret % M
        return dfs(0, max_num)-dfs(0, min_num-1)

    def test(self, **kg):
        return self.count(**kg)

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
