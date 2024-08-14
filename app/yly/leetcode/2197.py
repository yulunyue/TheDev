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
# 定义函数


def lcm(x, y):

    #  获取最大的数
    if x > y:
        greater = x
    else:
        greater = y

    while(True):
        if((greater % x == 0) and (greater % y == 0)):
            lcm = greater
            break
        greater += 1

    return lcm


class Solution:
    def get_cases(self):
        return [
            dict(nums=[287, 41, 49, 287, 899, 23, 23,
                 20677, 5, 825], result=[2009, 20677, 825]),
            dict(nums=[6, 4, 3, 2, 7, 6, 2], result=[12, 7, 6])
        ]

    def replaceNonCoprimes(self, nums: List[int]) -> List[int]:
        if len(nums) == 1:
            return nums
        ret = []
        tmp = nums[0]
        for i in range(1, len(nums)):
            if math.gcd(nums[i], tmp) > 1:
                tmp = lcm(tmp, nums[i])
            else:
                ret.append(tmp)
                while len(ret) >= 2 and math.gcd(ret[-1], ret[-2]) > 1:
                    ret.append(lcm(ret.pop(), ret.pop()))
                tmp = nums[i]
            if i == len(nums)-1:
                ret.append(tmp)
                while len(ret) >= 2 and math.gcd(ret[-1], ret[-2]) > 1:
                    ret.append(lcm(ret.pop(), ret.pop()))

        return ret

    def test(self, **kg):
        return self.replaceNonCoprimes(**kg)

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
