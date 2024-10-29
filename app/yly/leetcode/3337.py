

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
    DEV = True
except:
    DEV = False

    class SolutionBase:
        def input(self):
            return input()

        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            pass


class Solution(SolutionBase):
    uri = "https://leetcode.cn/problems/total-characters-in-string-after-transformations-ii/description/"
    gameid = ''

    def get_cases(self):
        return [
            dict(s="abcyy", t=2, nums=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2], result=7)
        ]

    def lengthAfterTransformations(self, s: str, t: int, nums: List[int]) -> int:
        ord_a = ord('a')
        n = 26
        dp_map = [[inf]*n for _ in range(n)]
        for i, v in enumerate(nums):
            for j in range(v):
                dp_map[i][(j+1+i) % 26] = 1
        s = [ord(v)-ord_a for v in s]

        def dijkstra(start):
            dist = dp_map[start]
            q = [(1, i) for i, v in enumerate(dist) if v == 1]
            while q:
                cost, u = heapq.heappop(q)
                if cost > dist[u]:
                    continue
                for i in range(nums[u]):
                    v = (i+1+u) % 26
                    target = cost + 1
                    if target < dist[v]:
                        dist[v] = target
                        heapq.heappush(q, (dist[v], v))
            return dist
        for i in range(n):
            dijkstra(i)
        self.log(dp_map)

    def execute(self, *args, **kw):
        return self.lengthAfterTransformations(*args, **kw)


if __name__ == '__main__':
    Solution().run()
