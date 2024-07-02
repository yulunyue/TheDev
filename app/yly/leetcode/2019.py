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
            dict(s="4+8*8+8*8+8*4+4*8+8*8+8", answers=[268, 936, 768, 776, 268, 34, 268, 936, 460, 268, 804, 268, 712, 750, 268, 1000, 729, 520, 268, 268, 868, 760, 800, 908, 664, 268, 492, 676, 800, 904, 268, 268, 900, 376, 714, 268, 318, 268, 656, 544, 268, 268, 359, 904, 832, 992, 268, 484, 913, 268, 268, 712, 736, 712, 268, 653, 800, 844, 268, 919, 268,
                 664, 888, 900, 868, 772, 928, 968, 932, 936, 832, 268, 664, 936, 652, 268, 544, 563, 876, 520, 172, 855, 868, 355, 813, 268, 268, 7, 964, 319, 888, 940, 968, 740, 268, 268, 268, 268, 664, 268, 548, 268, 268, 680, 992, 268, 268, 442, 268, 575, 583, 572, 736, 960, 590, 880, 936, 268, 268, 680, 652, 159, 548, 800, 240, 960, 768, 268], result=318),
            dict(s="7+3*1*2", answers=[20, 13, 42], result=7)
        ]

    def scoreOfStudents(self, s: str, answers: List[int]) -> int:
        op = []
        nums = []
        ret_map = defaultdict(int)
        ret = 0
        for v in s:
            if v == '+' or v == '*':
                op.append(v)
            else:
                nums.append(int(v))

        @lru_cache(None)
        def dfs(ops, nums):
            if not ops:
                ret_map[nums[0]] = 2
            for i in range(len(ops)):
                v = nums[i] + nums[i+1] if ops[i] == '+' else nums[i]*nums[i+1]
                if v <= 1000:
                    dfs(ops[:i]+ops[i+1:], nums[:i]+(v,)+nums[i+2:])
        dfs(tuple(op), tuple(nums))
        ret_map[eval(s)] = 5
        for a in answers:
            ret += ret_map[a]
        return ret

    def test(self, **kg):
        return self.scoreOfStudents(**kg)

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
