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
            dict(
                flowers=[5, 5, 15, 1, 9], newFlowers=36, target=12, full=9, partial=2, result=58,
            ),
            dict(
                flowers=[20, 1, 15, 17, 10, 2, 4, 16, 15, 11],
                newFlowers=2,
                target=20,
                full=10,
                partial=2, result=14
            ),
            dict(flowers=[13],
                 newFlowers=18,
                 target=15,
                 full=9,
                 partial=2,
                 result=28),
            dict(flowers=[1, 3, 1, 1], newFlowers=7, target=6, full=12, partial=1,
                 result=14),
            dict(flowers=[2, 4, 5, 3],
                 newFlowers=10,
                 target=5,
                 full=2,
                 partial=6,
                 result=30)
        ]

    def maximumBeauty(self, flowers: List[int], newFlowers: int, target: int, full: int, partial: int) -> int:
        n = len(flowers)
        flowers.sort()
        partial_need = [0]
        ret = flowers[0]*partial
        for i in range(n):
            flowers[i] = min(flowers[i], target)
            partial_need.append(partial_need[-1]+flowers[i])
        if n*target <= newFlowers+partial_need[-1]:
            ret = max(ret, n*full)
        partial_num = target-1
        # self.log(flowers)
        # self.log(partial_need)
        # self.log(ret)
        for i in range(n, 0, -1):
            full_has = partial_need[n]-partial_need[i]
            full_need = target*(n-i)-full_has
            if full_need < newFlowers:
                break
            rest = newFlowers-full_need
            # partial_num = min(partial_num, flowers[i-1])
            j = i
            while partial_num*j-partial_need[j] > rest:
                partial_num -= 1
                j = bisect.bisect_left(flowers[:i], partial_num)

            ret = max(ret, (n-i)*full+partial_num*partial)
            self.log(i, flowers[i-1], n-i, partial_num, ret, rest)
        return ret

    def test(self, **kg):
        return self.maximumBeauty(**kg)

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
