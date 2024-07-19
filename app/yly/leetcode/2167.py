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
            dict(s="1100101", result=5),
            dict(s="111111101001", result=10)
        ]

    def minimumTime(self, s: str) -> int:
        '''
        i+n-j+2*(pre[j]-pre[i]) i<j
        '''
        n = len(s)
        one_count = [0]
        for v in s:
            one_count.append(one_count[-1]+int(v))
        ans = mid = n//2
        for i in range(mid):
            if s[i] == '0':
                continue
            ans = min(ans, i+1+(one_count[mid]-one_count[i+1])*2)
        ans1 = n-mid
        for i in range(n-1, mid-1, -1):
            if s[i] == '0':
                continue
            ans1 = min(ans1, n-i+(one_count[i]-one_count[mid])*2)
        return ans+ans1

    def test(self, **kg):
        return self.minimumTime(**kg)

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
