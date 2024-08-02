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
            dict(tires=[[2, 3], [3, 4]], changeTime=5, numLaps=4,
                 result=21)
        ]

    def minimumFinishTime(self, tires: List[List[int]], changeTime: int, numLaps: int) -> int:
        '''
        numLaps = ni1+n2
        ret = n
        '''
        n = len(tires)
        tires.sort()
        q = []
        for i in range(n):
            if q and tires[i][1] >= q[-1][1]:
                continue
            q.append(tires[i]+[tires[i][1]])
        step = []
        for i in range(numLaps):
            hp = []
            for v in q:
                v3 = v[0]*(v[2]-1)//(v[1]-1)
                heapq.heappush(hp, v3)
                v[2] *= v[1]
            step.append(heapq.heappop(hp)+changeTime)
        self.log(step)

    def test(self, **kg):
        return self.minimumFinishTime(**kg)

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
