from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
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


class TieTree:
    END = '_END'
    SUM = '_SUM'

    def __init__(self, size) -> None:
        self.size = size
        self.map = dict()

    def get_num_str(self, s: int):
        ss = bin(s)[2:]
        s1 = '0'*(self.size-len(ss))+ss
        return s1

    def add(self, s: int):
        tmp = self.map
        s1 = self.get_num_str(s)
        for i, v in enumerate(s1):
            if v not in tmp:
                tmp[v] = dict()
            if i == len(s1)-1:
                tmp[v][self.END] = s1
            tmp = tmp[v]
            if TieTree.SUM not in tmp:
                tmp[TieTree.SUM] = 0
            tmp[TieTree.SUM] += 1

    def query_max(self, v):
        s1 = self.get_num_str(v)
        if not self.map:
            return -1
        ret = 0
        tmp = self.map
        for i, v in enumerate(s1):
            aimv = '1' if v == '0' else '0'
            if aimv in tmp:
                tmp = tmp[aimv]
                ret += 1 << (self.size-i-1)
            elif v in tmp:
                tmp = tmp[v]
            else:
                break
        return ret

    def get_count_small(self, v, x):
        pass


class Solution:
    def get_cases(self):
        return [
            [[1, 4, 2, 7], 2, 6, 6]
        ]

    def countPairs(self, nums: List[int], low: int, high: int) -> int:

        def find(x: int):
            res = 0
            ti = TieTree()
            for i in range(1, len(nums)):
                ti.add(nums[i]-1)
                res += ti.get_count_small(nums[i], x)
            return res

        return find(high)-find(low-1)


>>>>>>>> 57b3861507dde46c9739ba962f4befd30cdd8f14: app/yly/leetcode/1803.py

   def check(self, *args):
        pass

    def test(self, *args):
        return self.countPairs(*args)

    def __init__(self) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s):
        if not self.local_debug or len(self.logs) >= 2048:
            return
        self.logs += " ".join([str(v) for v in s])+"\n"

    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs = ""
            try:
                r = self.local_debug(*case[:-1])
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, case[-1]):
                self.check(*case, r)
                print(case, r)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
