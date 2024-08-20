from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
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
            dict(n=2, batteries=[3, 3, 3], result=4)
        ]

    def maxRunTime(self, n: int, batteries: List[int]) -> int:
        batteries.sort()
        sv = [0]
        for v in batteries:
            sv.append(sv[-1]+v)
        l, r = batteries[0], sv[-1]//n
        ans = 0
        while l <= r:
            self.log(l, r, ans)
            m = (l+r)//2
            idx = bisect.bisect_left(batteries, m)
            if (n-len(batteries)+idx)*m <= sv[idx]:
                ans = m
                l = m+1
            else:
                r = m-1
        return ans

    def test(self, **kg):
        return self.maxRunTime(**kg)

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s, tp: str = ""):
        if not self.local_debug or len(self.logs) >= 2048:
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
