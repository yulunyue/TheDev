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
            dict(
                n =4,meetings =[[18,19],[3,12],[17,19],[2,13],[7,10]],result=0
            ),
            dict(n =3,
meetings =[[1,20],[2,10],[3,5],[4,9],[6,8]],
result=1),
            dict(n = 2, meetings = [[0,10],[1,5],[2,7],[3,4]],result=0)
        ]


    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        RECORD_ENABLE = True
        meetings.sort()
        rooms=[[meetings[i][e],i] for i in range(n)]
        room_num=[0]*n
        for s,e in meetings:
            cur_time,idx=heapq.heappop(rooms)
            room_num[idx]+=1
            heapq.heappush(rooms,[max(cur_time,s)+e-s,idx])
            self.log(s,e,rooms)
        min_num=max(room_num)
        self.log(room_num)
        for i in range(n):
            if room_num[i]==min_num:
                return i
        # 

    def test(self, **kg):
        return self.mostBooked(**kg)

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
        from common.third_util.draw import Draw
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
