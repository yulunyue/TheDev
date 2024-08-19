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
            dict(favorite=[1, 0, 1, 2, 0], result=4),
            dict(favorite=[1, 2, 3, 0, 0], result=4)
        ]

    def xx(self, favorite: List[int]):
        n = len(favorite)
        in_degre = [0]*n
        for v in favorite:
            in_degre[v] += 1
        f_max = [0]*n
        q = [i for i, v in enumerate(in_degre) if v == 0]
        while q:
            idx = q.pop(0)
            in_degre[favorite[idx]] -= 1
            f_max[favorite[idx]] = f_max[idx]+1
            if in_degre[favorite[idx]] == 0:
                q.append(in_degre[favorite[idx]])
        ans = 0
        for i, v in enumerate(in_degre):
            if v == 0:
                continue
            cnt = 0
            max_n = f_max[i]
            while i != favorite[i] and in_degre[i] != 0:
                in_degre[i] = 0
                cnt += 1
                i = favorite[i]
                max_n = max(max_n, f_max[i])
            if cnt == 2:
                ans = max(ans, 2+max_n)
            else:
                ans = max(ans, cnt)
        return ans

    def test(self, **kg):
        return self.xx(**kg)

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
