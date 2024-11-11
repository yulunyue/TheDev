

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
MOD = (10**9)+7
try:
    from app.yly.manage import SolutionBase

except:

    class SolutionBase:
        DEV = False

        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            pass

        def watch(self):
            pass


class Solution(SolutionBase):
    uri = "https://leetcode.cn/problems/smallest-divisible-digit-product-ii/description/"
    gameid = ''

    def get_cases(self):
        return [
            dict(num="19", t=2, result="21"),
            dict(num="1", t=6, result="6"),
            dict(num="12", t=1968750, result="255555579"),
            dict(num="10", t=320, result="588"),
            dict(num="12355", t=50, result="12355"),
            dict(num="11111", t=26, result="-1"),
            dict(num="1234", t=256, result="1488")
        ]

    def execute(self):

        nums = {}
        for v in range(9, 1, -1):
            while self.t % v == 0:
                nums[v] = nums.get(v, 0)+1
                self.t = self.t//v
            if self.t == 1:
                break
        if self.t != 1:
            return "-1"
        for v in self.num:
            if v == 1:
                continue
            if v in nums:
                nums[v] -= 1
        if all(v <= 0 for v in nums.values()):
            return "".join(str(v) for v in self.num)

        # self.log(nums)

        def check(n, nms):
            ans = []
            for j in range(9, 1, -1):
                if j not in nms:
                    continue
                if nms[j] > n:
                    return
                ans = [j]*nms[j]+ans
                n -= nms[j]
            if n >= 0:
                return ans
        for i in range(len(self.num)-1, 0, -1):
            ni = self.num[i]
            if ni in nums:
                nums[ni] += 1
            for j in range(self.num[i], 10):
                nj = j
                if nj in nums:
                    nums[nj] -= 1
                s1 = check(len(self.num)-1-i, nums.copy())
                if s1 is not None:
                    s2 = self.num[:i]+[j]+s1
                    return "".join(str(v) for v in s2)
                if nj in nums:
                    nums[nj] += 1
        i = len(self.num)
        while True:
            s2 = check(i, nums.copy())
            if s2 is not None:
                return "".join(str(v) for v in s2)
            i += 1

    def init(self, num: str, t: int) -> str:
        self.num, self.t = [int(v) for v in num], t

    def smallestNumber(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
