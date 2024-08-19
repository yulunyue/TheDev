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
            dict(left=2, right=11, result="399168e2")
        ]

    def abbreviateProduct(self, left: int, right: int) -> str:
        ans = 1, 1

        def chen(ans, v):
            return int(str(ans[0]*v)[:20]), ans[1]*v % (10**5)
        cnt5 = cnt10 = 0
        lst = list(range(left, right+1))
        n = len(lst)
        for i in range(n):
            while lst[i] and lst[i] % 10 == 0:
                lst[i] //= 10
                cnt10 += 1
            while lst[i] and lst[i] % 5 == 0:
                lst[i] //= 5
                cnt5 += 1
        self.log(cnt5, cnt10, lst)
        for i in range(n):
            while cnt5 > 0 and lst[i] % 2 == 0:
                lst[i] = lst[i] // 2
                cnt5 -= 1
                cnt10 += 1
            ans = chen(ans, lst[i])

        ans = chen(ans, 5**cnt5)
        if len(str(ans[0])) <= 10:
            return str(ans[0])+'e'+str(cnt10)
        return str(ans[0])[:5]+'...'+str(ans[1])+'e'+str(cnt10)

    def test(self, **kg):
        return self.abbreviateProduct(**kg)

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
