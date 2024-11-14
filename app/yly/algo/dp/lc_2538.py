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
    from app.yly.algo.manage import SolutionBase
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
            dict(n=6, edges=[[0, 1], [1, 2], [1, 3], [3, 4], [
                 3, 5]], price=[9, 8, 7, 6, 10, 5], result=24.1),
        ]

    def execute(self, n: int, edges: List[List[int]], price: List[int]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建树
        ans = 0

        def dfs(x: int, fa: int):

            nonlocal ans

            max_s1 = p = price[x]

            max_s2 = 0

            for y in g[x]:

                if y == fa:
                    continue

                s1, s2 = dfs(y, x)

                # 前面最大带叶子的路径和 + 当前不带叶子的路径和

                # 前面最大不带叶子的路径和 + 当前带叶子的路径和

                ans = max(ans, max_s1 + s2, max_s2 + s1)

                max_s1 = max(max_s1, s1 + p)

                max_s2 = max(max_s2, s2 + p)  # 这里加上 p 是因为 x 必然不是叶子
            self.log(fa, x, max_s1, max_s2, ans)
            return max_s1, max_s2

        dfs(0, -1)

        return ans

    def maxOutput(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
