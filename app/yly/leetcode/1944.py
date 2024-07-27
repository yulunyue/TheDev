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
            dict(heights=[10, 6, 8, 5, 11, 9], result=[3, 1, 2, 1, 1, 0])
        ]

    def canSeePersonsCount(self, heights: List[int]) -> List[int]:
        n = len(heights)
        res = [0]*n
        stack = []
        for i in range(n-1, -1, -1):
            count = 0
            while stack and heights[i] >= stack[-1]:
                stack.pop()
                count += 1
            res[i] = count+1 if stack else count
            stack.append(heights[i])
        return res

    def canSeePersonsCount(self, heights: List[int]) -> List[int]:
        n = len(heights)
        q = []
        ret = [0]*n
        for i in range(n-1, -1, -1):
            # while len(q) > 1 and q[-2] > heights[i]:
            #     q.pop()
            self.log(i, heights[i], q)
            ret[i] = bisect.bisect_right(q, heights[i])
            if ret[i] < len(q):
                ret[i] += 1
            while q and q[0] < heights[i]:
                q.pop(0)
            q.insert(0, heights[i])
        return ret

    def test(self, **kg):
        return self.canSeePersonsCount(**kg)

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
            ep = case.pop("result")
            try:
                r = self.local_debug(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, ep):
                print(case, r, ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
