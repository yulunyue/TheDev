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
        l1, l2 = bisect.bisect_left(nums1, 0), bisect.bisect_right(nums1, 0)
        r1, r2 = bisect.bisect_left(nums2, 0), bisect.bisect_right(nums2, 0)
        nums11, nums12 = [-v for v in nums1[:l1]], nums1[l2:]
        nums21, nums22 = [-v for v in nums2[:r1]], nums2[r2:]
        small_zero_num = len(nums11)*len(nums22)+len(nums12)*len(nums21)

        def uitl(array1, array2, array3, array4, n):
            self.log(array1, array2, array3, array4, n)
            return 0
        if k <= small_zero_num:
            return -uitl(nums11, nums22, nums21, nums12, small_zero_num-k)
        elif k <= small_zero_num+(l2-l1)*(r2-r1):
            return 0
        return uitl(nums11, nums21, nums12, nums22, k)

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
