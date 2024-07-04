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
            dict(s1="112s", s2="g841",
                 result=true),
            dict(s1="internationalization", s2="i18n",
                 result=True),
            dict(s1="a5b", s2="c5b",
                 result=false)
        ]

    @lru_cache(None)
    def stonum(self, s: str):
        if len(s) == 0:
            return []
        if len(s) == 1 or (len(s) > 1 and not s[1].isdigit()):
            return [[int(s[0]), 10]]
        ret = []
        c = int(s[0])
        for a, b in self.stonum(s[1:]):
            ret.append([c+a, 10])
            ret.append([c*b+a, b*10])
        return ret

    def possiblyEquals(self, s1: str, s2: str) -> bool:

        def dfs(s1: str, s2: str):
            ret = False
            if not s1 or not s2:
                ret = s1 == "" and s2 == ""
            elif s1[0] == s2[0]:
                ret = dfs(s1[1:], s2[1:])
            elif s1[0].isdigit() and s2[0].isdigit():
                i1, i2 = s1
                v1 = set([d[0] for d in self.stonum(s1)])
                v2 = set([d[0] for d in self.stonum(s2)])
                for va in v1:
                    for vb in v2:
                        if va < vb:
                            pass
                self.log(s1, v1, s2, v2)
            elif s1[0].isdigit() or s2[0].isdigit():
                if s2[0].isdigit():
                    s1, s2 = s2, s1
                i = 0
                v = 0
                while i < len(s1) and s1[i].isdigit():
                    v = v*10+int(s1[i])
                    i += 1
                    if v < len(s2) and dfs(s1[i:], s2[v:]):
                        ret = True
                        break

            self.log(ret, s1, s2)
            return ret
        return dfs(s1, s2)

    def possiblyEquals(self, s1: str, s2: str) -> bool:
        def util(i, s: str):
            j = i
            while i < len(s) and s[i].isdigit():
                i += 1
            return i, list(set([v[0] for v in self.stonum(s[j:i])])) if j != i else ""

        def dfs(i1, i2, v1, v2):
            ret = False
            i1, s3 = util(i1, s1)
            i2, s4 = util(i2, s2)
            s3 += v1
            s4 += v2
            for i in range(len(s3)):
                dfs(i1, i2+1, s3[:i]+[s3[i]-1]+s3[i+1:], v2)
            self.log(ret, s1[i1:], s2[i2:], v1, v2, s3, s4)
            return ret
        return dfs(0, 0, [], [])

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
