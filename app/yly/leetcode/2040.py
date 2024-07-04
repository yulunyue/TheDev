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
            dict(nums1=[2, 5], nums2=[3, 4], k=2,
                 result=8),
        ]

    def kthSmallestProduct(self, nums1: List[int], nums2: List[int], k: int) -> int:
        l1 = bisect.bisect_left(nums1, 0)
        l2 = bisect.bisect_left(nums2, 0)
        nums11, nums12 = nums1[:l1], nums1[l1:]
        nums21, nums22 = nums2[:l2], nums2[l2:]
        small_zero_num = len(nums11)*len(nums22)+len(nums12)*len(nums21)
        self.log(small_zero_num, k)
        if small_zero_num >= k:
            pass
        else:
            k -= small_zero_num
            min_value, max_value = inf, -inf
            if nums12 and nums22:
                min_value = min(min_value, nums12[0]*nums22[0])
                max_value = max(max_value, nums12[-1]*nums22[-1])
            if nums11 and nums21:
                min_value = min(min_value, nums11[-1]*nums21[-1])
                max_value = max(max_value, nums12[0]*nums22[0])
            while k:
                l = (min_value+max_value)//2

    def test(self, **kg):
        return self.kthSmallestProduct(**kg)

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
