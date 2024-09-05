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
            dict(nums=[5, 12, 8, 5, 5, 1, 20, 3,
                 10, 10, 5, 5, 5, 5, 1], result=27),
            dict(nums=[3, 12, 30, 17, 21], result=2)
        ]

    def countPairs(self, nums: List[int]) -> int:
        use_nums = []
        for v in nums:
            tmp = set()
            vs = str(v)
            vt = len(vs)
            for i in range(vt):
                for j in range(i+1, vt):
                    vc = int(vs[i])-int(vs[j])
                    if vc == 0:
                        continue
                    vi = vc*(10**(vt-i-1))
                    vj = -vc*(10**(vt-j-1))
                    tmp.add(v-vi-vj)
            use_nums.append(tmp)
        ret = 0
        n = len(nums)
        for i in range(n):
            for j in range(i+1, n):
                if nums[i] == nums[j]:
                    ret += 1
                elif nums[i] in use_nums[j] or nums[j] in use_nums[i]:
                    ret += 1
        return ret

    def test(self, **kg):
        return self.countPairs(**kg)

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
