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
            dict(n=11, firstPlayer=2, secondPlayer=4, result=[3, 4])
        ]

    def earliestAndLatest(self, n: int, firstPlayer: int, secondPlayer: int) -> List[int]:
        firstPlayer -= 1
        secondPlayer -= 1

        @lru_cache(None)
        def dfs(s):
            p = [i for i in range(n) if s & (1 << i) == 0]
            state = {s}
            for i in range(len(p)//2):
                cur = set()
                j = len(p)-i-1
                if p[i] == firstPlayer and p[j] == secondPlayer:
                    return [1, 1]
                for m in state:
                    if p[i] != firstPlayer and p[i] != secondPlayer:
                        cur.add(m | 1 << p[i])
                    if p[j] != firstPlayer and p[j] != secondPlayer:
                        cur.add(m | 1 << p[j])
                state = cur

            ansn, ansx = [n, -1]
            for st in state:
                mn, mx = dfs(st)
                if ansn > 1+mn:
                    ansn = 1+mn
                if ansx < 1+mx:
                    ansx = 1+mx
            # self.log(s, ansn, ansx)
            return ansn, ansx
        return dfs(0)

    def test(self, **kg):
        return self.earliestAndLatest(**kg)

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
