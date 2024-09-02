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
<<<<<<<< HEAD:app/yly/leetcode/2321.py
            dict(nums1=[60, 60, 60], nums2=[10, 90, 10], result=210)
        ]

    def xx(self, nums1, nums2):
        s1 = sum(nums1)
        s2 = sum(nums2)
        max_sc1 = 0
        max_sc2 = 0
        sc1 = 0
        sc2 = 0
        for i in range(len(nums1)):
            c = nums2[i]-nums1[i]
            sc1 += c
            sc2 -= c
            if sc1 < 0:
                sc1 = 0
            if sc2 < 0:
                sc2 = 0
            max_sc1 = max(sc1, max_sc1)
            max_sc2 = max(sc2, max_sc2)
            # self.log(ret, sc, c)
        return max(s1+max_sc1, s2+max_sc2)

    def test(self, **kg):
        return self.xx(**kg)
========
            dict(s = "aabb",result=2),
            dict(s = "letelt",result=2)
        ]
    def minMovesToMakePalindrome(self, s: str) -> int:
        s2=defaultdict(list)
        for i,v in s:
            s2[v].append(i)
            
    def test(self, **kg):
        return self.minMovesToMakePalindrome(**kg)
>>>>>>>> 5d3e63ef0bebeb78add34e5a98dae88cbdfb43f9:app/yly/leetcode/2193.py

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
