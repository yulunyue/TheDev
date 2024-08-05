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


class IntervalTree:
    '''
                    16
        8
    4        12            20
  2   6   10    14     18
 1 3 5 7 9 11 13  15 17  19  21
    '''

    def __init__(self, size, default_value) -> None:
        self.array = [default_value]*size
        self.size = size

    def update_value(self, l, v):
        while l < self.size:
            self.array[l] = v(self.array[l])
            l += l & -l

    def query_value(self, l, f, init_value):
        ret = init_value
        while l > 0:
            ret = f(ret, self.array[l])
            l -= l & -l
        return ret

    def query_sum(self, l):
        return self.query_value(l, lambda a, b: a+b, 0)

    def add_value(self, l, v):
        self.update_value(l, lambda a: a+v)


class Solution:
    def get_cases(self):
        return [
            dict(s="aabb", result=2),
            dict(s="letelt", result=2)
        ]

    def minMovesToMakePalindrome(self, s: str) -> int:
        n = len(s)
        s = list(s)
        ct = defaultdict(list)
        # it = IntervalTree(n+1, 0)
        it = [0]*n
        ret = 0
        for i, v in enumerate(s):
            ct[v].append(i)
        for i in range(n):
            v = s[i]
            if not v:
                continue
            if len(ct[v]) == 1:
                continue
            l, r = ct[v].pop(0), ct[v].pop()
            s[l] = s[r] = ""
            # all_num = it.query_sum(n)
            # l1 = l-all_num+it.query_sum(l+1)
            # r1 = r-all_num+it.query_sum(r+1)
            # it.add_value(r+1, 1)
            l1, r1 = l-it[l], r-it[r]
            r2 = n - l1 - 1
            for j in range(r1+1, r2+1):
                it[j] += 1
            self.log(l, r1, r2, it)
            ret += r2-r1
        return ret

    def test(self, **kg):
        return self.minMovesToMakePalindrome(**kg)

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
