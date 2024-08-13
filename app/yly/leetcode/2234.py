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
        partial_need = [flowers[0]]
        full_need = [target-flowers[-1]]
        for i in range(1, n):
            partial_need.append(partial_need[-1]+flowers[i])
            full_need.append(full_need[-1]+target-flowers[-i-1])
        self.log(partial_need)
        self.log(full_need)
        ret = 0
        if n*target <= newFlowers+partial_need[-1]:
            ret = n*full
        flow_min = partial_need[0]
        while flow_min < target:
            if flow_min+n*target-target <= newFlowers+partial_need[-1]:
                full_num = n-1
            else:
                partial_num = bisect.bisect_right(flowers, flow_min)
                partial_use = partial_num*flow_min-partial_need[partial_num-1]
                full_can_use = newFlowers-partial_use
                if full_can_use < 0:
                    break
                full_num = bisect.bisect_right(full_need, full_can_use)
                if partial_num+full_num > n:
                    full_num = n-partial_num
            tmp = flow_min*partial+full_num*full
            ret = max(ret, tmp)
            self.log(flow_min, full_num, ret)
            flow_min += 1

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
