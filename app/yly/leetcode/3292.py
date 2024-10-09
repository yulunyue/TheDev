from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
try:
    from app.yly.leetcode.manage import SolutionBase
except:
    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def run(self):
            pass
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(words=["abc", "aaaaa", "bcdef"],
                 target="aabcdabc",
                 result=3)
        ]

    def execute(self, words: List[str], target: str) -> int:
        mp = dict()
        for word in words:
            tmp = mp
            for w in word:
                if w not in tmp:
                    tmp[w] = dict()
                tmp = tmp[w]
        n = len(target)
        # self.log(mp)

        @lru_cache(None)
        def dfs(i):
            if i == n:
                return 0
            ans = inf
            tmp = mp
            for j in range(i, n):
                if target[j] not in tmp:
                    break
                tmp = tmp[target[j]]
                ans = min(ans, 1+dfs(j+1))
            # self.log(ans, target[i:])
            return ans
        ans = dfs(0)
        return -1 if ans == inf else ans

    def minValidStrings(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
