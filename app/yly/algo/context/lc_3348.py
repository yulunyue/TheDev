

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
            dict(num="30", t=9, result="33"),
            dict(num="19", t=2, result="21"),
            dict(num="22", t=80, result="258"),

            dict(num="1", t=6, result="6"),
            dict(num="12", t=1968750, result="255555579"),
            dict(num="10", t=320, result="588"),
            dict(num="12355", t=50, result="12355"),
            dict(num="11111", t=26, result="-1"),
            dict(num="1234", t=256, result="1488")
        ]

    def execute(self):
        nums = {7: 0, 5: 0, 3: 0, 2: 0}
        chu_mp = {9: [3, 2], 8: [2, 3], 6: [3, 1], 4: [2, 2]}
        for v in nums.keys():
            while self.t % v == 0:
                nums[v] = nums.get(v, 0)+1
                self.t = self.t//v
            if self.t == 1:
                break
        if self.t != 1:
            return "-1"

        def add(v, nms: dict, c):
            if v == 1:
                return
            add_one = 1
            s1 = v
            if v in chu_mp:
                s1, add_one = chu_mp[v]
            if v == 6:
                nms[2] = nms.get(2, 0)+c
            nms[s1] = nms.get(s1, 0)+add_one*c

        nums1 = nums.copy()
        for v in self.num:
            add(v, nums1, -1)
        if all(v <= 0 for v in nums.values()):
            return "".join(str(v) for v in self.num)

        def check(n1, nms):
            n = n1
            ans = []
            for j in range(9, 1, -1):
                if j not in nms or nms[j] <= 0:
                    continue
                if nms[j] > n:
                    return
                ans = [j]*nms[j]+ans
                n -= nms[j]
            if n >= 0:
                # self.log(n1, nms, ans)
                return ans+[1]*(n1-len(ans))
        for i in range(len(self.num)-1, -1, -1):
            add(self.num[i], nums1, 1)
            for j in range(self.num[i]+1, 10):
                add(j, nums1, -1)
                s1 = check(len(self.num)-1-i, nums1)
                if s1 is not None:
                    s2 = self.num[:i]+[j]+s1
                    return "".join(str(v) for v in s2)
                add(j, nums1, 1)

        i = len(self.num)+1
        while True:
            s2 = check(i, nums1.copy())
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
