

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
        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            pass

        def watch(self, watch_ins, _type="text", _ins=None, **kg):
            pass


class Solution(SolutionBase):
    uri = ""
    gameid = ''

    def get_cases(self):
        return [
            dict(X=3, Y=4, circles=[[2, 1, 1]], result=True)
        ]

    def execute(self):
        def dis(x1, x2, y1, y2):
            return (y1-y2) * (y1-y2)+(x1-x2)*(x1-x2)
        for i in range(self.n):
            xi, yi, ir = self.circles[i]
            left_c = -ir <= xi <= ir and 0 <= yi <= self.y
            right_c = -ir <= xi-self.x and 0 <= yi <= self.y
            top_c = -ir <= yi <= ir and 0 <= xi <= self.x
            bottom_c = -ir <= yi-self.x <= ir and 0 <= xi <= self.x
            if (left_c and top_c) or (right_c and bottom_c):
                return False

            for j in range(i+1, self.n):
                xj, yj, jr = self.circles[j]
                if ir+jr <= dis(xi, xj, yi, yj):
                    self.g[i].append(j)
                    self.g[j].append(i)

    def init(self, X: int, Y: int, circles: List[List[int]], result=None) -> bool:
        self.x = X
        self.y = Y
        self.n = len(circles)
        self.g = [[] for _ in range(self.n+2)]
        self.circles = circles

    def get_watch(self):
        return [
            self.watch(
                self.circles
            )
        ]

    def canReachCorner(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
