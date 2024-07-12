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
            dict(s="leetcode", power=7, modulo=20, k=2, hashValue=0,
                 result="ee"),
            dict(s="fbxzaad", power=31, modulo=100, k=3, hashValue=32,
                 result="fbx")
        ]

    def subStrHash(self, s: str, power: int, modulo: int, k: int, hashValue: int) -> str:
        c = 1
        a = 0
        int_a = ord('a')-1

        for i in range(k):
            a = a+(ord(s[i])-int_a)*c
            c = c*power
        if a % modulo == hashValue:
            return s[:k]
        c = c//power
        for j in range(k, len(s)):
            # self.log(a, c, (ord(s[j-k])-int_a)*c)
            a = (a-ord(s[j-k])+int_a)//power+(ord(s[j])-int_a)*c
            self.log(a, s[j-k+1:j+1])
            if a % modulo == hashValue:
                return s[j-k+1:j+1]

    def test(self, **kg):
        return self.subStrHash(**kg)

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
