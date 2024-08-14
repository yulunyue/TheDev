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
            dict(tires=[[2, 3], [3, 4]], changeTime=5, numLaps=4, result=21),
            dict(tires=[[3, 4], [84, 2], [63, 8], [72, 8], [82, 7], [83, 6], [23, 2], [77, 5], [51, 10], [28, 2], [47, 9], [8, 3], [48, 3], [56, 3], [8, 10], [66, 6], [92, 9], [44, 6], [23, 5], [5, 6], [86, 9], [13, 10], [91, 3], [2, 2], [8, 4], [67, 8], [63, 6], [
                 52, 5], [42, 10], [3, 9], [66, 5], [35, 10], [63, 6], [65, 6], [22, 8], [40, 9], [43, 4], [73, 9], [81, 5], [32, 2], [30, 5], [80, 9], [50, 4], [35, 4], [52, 7], [11, 5], [7, 8], [68, 3], [54, 8], [49, 8]], changeTime=90, numLaps=87, result=2526)
        ]

    def minimumFinishTime(self, tires: List[List[int]], changeTime: int, numLaps: int) -> int:
        tires.sort()
        i, k, a = 0, inf, [0] * (numLaps + 1)
        for t in tires:
            if t[1] < k:
                k = t[1]
                tires[i] = t
                i += 1
        del tires[i:]
        tires.reverse()
        a[1] = tires[-1][0]

        @cache
        def f(x):
            m, i = min(((r**x - 1) // (r - 1) * f, j)
                       for j, (f, r) in enumerate(tires))
            del tires[i + 1:]
            return m

        k = 2
        for x in range(2, numLaps + 1):
            m = min(a[i] + a[x - i]
                    for i in range(1, min(k, x // 2 + 1))) + changeTime
            while m > f(k):
                if k == x:
                    m = f(k)
                    break
                m = min(m, a[k] + a[x - k] + changeTime)
                k += 1
            a[x] = m
        return a.pop()

    def minimumFinishTime(self, tires: List[List[int]], changeTime: int, numLaps: int) -> int:
        MAX_T = 18
        tires = sorted([[v[0], v[1], v[1]] for v in tires])
        laps = []
        for _ in range(MAX_T):
            laps.append(inf)
            for tire in tires:
                laps[-1] = min(laps[-1], tire[0]*(tire[2]-1) //
                               (tire[1]-1))
                tire[2] *= tire[1]
        self.log(laps)

        @lru_cache(None)
        def dfs(n):
            if n <= 0:
                return 0
            ret = inf
            for j in range(MAX_T):
                if j > n:
                    continue
                ret = min(ret, changeTime+dfs(n-j-1)+laps[j])
            # self.log(n, ret)
            return ret
        return dfs(numLaps)-changeTime

    def test(self, **kg):
        return self.minimumFinishTime(**kg)

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
