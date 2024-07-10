from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
from functools import lru_cache
from sortedcontainers import SortedList
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
            [[[9, 9], [6, 7], [5, 6], [2, 5], [3, 3]],
                [6, 1, 1, 1, 9], [2, -1, -1, -1, 1]],
            [[[4, 5], [5, 8], [1, 9], [8, 10], [1, 6]],
                [7, 9, 3, 9, 3], [4, 3, 6, 3, 6]],
            [[[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22], [2, -1, 4, 6]]
        ]

    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals = sorted([[v[1]-v[0], v[0], v[1]] for v in intervals])
        queries = sorted([[q, i] for i, q in enumerate(queries)])
        ret = [-1]*len(queries)
        self.log(intervals)
        self.log(queries)
        for q, i in queries:
            while intervals and intervals[0][1] < q:
                intervals.pop(0)

            tmp = inf
            # for a, b in intervals:
            #     if a-b > q:
            #         continue
            #     tmp = min(b+1, tmp)
            # if tmp != inf:
            #     ret[i] = tmp
            self.log(i, q, intervals, ret[i])
        return ret

    def check(self, *args):
        pass

    def test(self, *args):
        return self.minInterval(*args)

    def init(self, *args):
        pass

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        self.init(*args)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s, tp: str = ""):
        if not self.local_debug or len(self.logs) >= 2048:
            return
        if tp.startswith('bar'):
            self.draw_bar(s[0], tp)
        self.logs += " ".join([str(v) for v in s])+"\n"

    def draw_bar(self, s, tp):
        from common.tool.draw import Draw
        Draw().draw_bar_chart(s).save(f"data/log/{tp}.png")

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
