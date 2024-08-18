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
            dict(s1='l123e', s2='44', result=true),
            dict(s1="internationalization", s2="i18n", result=true),
            dict(s1="112s", s2="g841", result=true),

        ]

    def possiblyEquals(self, s1: str, s2: str) -> bool:

        def u(s: str):
            if 2 < len(s) and s[2].isdigit() and s[1].isdigit() and s[0].isdigit():
                a, b, c = int(s[0]), int(s[1]), int(s[2])
                return 3, [a+b+c, a*10+b+c, a*100+b*10+c]
            if 1 < len(s) and s[1].isdigit() and s[0].isdigit():
                a, b = int(s[0]), int(s[1])
                return 2, [a+b, a*10+b]
            if s and s[0].isdigit():
                return 1, [int(s[0])]
            return 0, []

        @lru_cache(None)
        def dfs(i1, i2, cha):
            if i1 >= len(s1) or i2 >= len(s2):
                return i1 == len(s1) and i2 == len(s2)
            a1, b1 = u(s1[i1:])
            a2, b2 = u(s2[i2:])
            i1 += a1
            i2 += a2
            self.log(s1[i1:], s2[i2:], b1, b2, a1, a2, cha)
            if not b1 and not b2:
                if s1[i1] != s2[i2]:
                    return False
                if cha > 0:
                    return dfs(i1+1+cha, i2+1, 0)
                return dfs(i1+1, i2+1+cha, 0)
            elif not b1:
                ct = 0
                while not s1[i1+ct].isdigit():
                    ct += 1
                for n in b2:
                    if dfs(i1+ct, i2, n-ct-cha):
                        return True
            elif not b2:
                ct = 0
                while not s1[i1+ct].isdigit():
                    ct += 1
                # for n in b2:
                #     if dfs(i1+ct, i2, 0):
                #         return True
            else:
                pass
                # for c1 in b1:
                #     for c2 in b2:
                #         if dfs(i1, i2, c1-c2):
                #             return True
            return False
        return dfs(0, 0, 0)

    def test(self, **kg):
        return self.possiblyEquals(**kg)

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
                print(case, 'result', r, 'except', ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
