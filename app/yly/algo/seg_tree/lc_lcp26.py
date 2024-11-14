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


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(SolutionBase):
    def get_cases(self):
        return [
        ]

    def execute(self, root: TreeNode) -> int:
        self.res = 0
        self.s = 1  # 根是否要加一个

        def dfs(node: TreeNode):
            if not node:
                return 0
            l = dfs(node.left)
            r = dfs(node.right)
            # 这是一个三叉
            if node.left and node.right:
                # 左右如果目前都没有，那必须左右至少有一个
                if (not l) and (not r):
                    self.res += 1
                # 左右不是俩都有，那无论如何根得加一个
                if not (l and r):
                    self.s = 1
                else:
                    self.s = 0
                return True
            return l or r

        l = dfs(root.left)
        r = dfs(root.right)

        # 如果左右都有，根就不需要了
        if l and r:
            return self.res
        # 如果左右只有一个，那么我们就拿那棵没有的树当父树然后 + s（对父树有需求+1，没需求不加）
        else:
            return self.res + self.s

    def navigation(self, *args, **kg):

        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
