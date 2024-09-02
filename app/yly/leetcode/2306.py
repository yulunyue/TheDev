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
            dict(ideas=['a', 'b'], result=0),
            dict(ideas=["coffee", "donuts", "time", "toffee"], result=6)
        ]
    def distinctNames(self, ideas: List[str]) -> int:
        ct = defaultdict(int)
        bad = [[0]*26 for _ in range(26)]
        size = [0]*26
        ans = 0
        for v in ideas:
            v0 = ord(v[0])-ord('a')
            size[v0] += 1
            mask = ct[v[1:]]
            ct[v[1:]] |= 1 << v0
            for j in range(26):
                if mask >> j & 1:
                    bad[v0][j] += 1
                    bad[j][v0] += 1
        for i, b in enumerate(bad):
            for j, m in enumerate(b[:i]):
                ans += (size[i]-m)*(size[j]-m)
        return ans*2

    def test(self, **kg):
        return self.distinctNames(**kg)

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
