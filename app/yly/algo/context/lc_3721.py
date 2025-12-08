from common.util.export import MockCf, List, CT, math
from common.algo.base.segtree import SegTreeNode


class T(SegTreeNode):
    min = max = 0

    def do(self, v):
        self.min += v
        self.max += v
        self.todo += v

    def up(self):
        self.min = CT.min(self.left.min, self.right.min)
        self.max = CT.max(self.left.max, self.right.max)

    def find(self, ql, qr, target):
        if not self.min <= target <= self.max:
            return -1
        return super().find(ql, qr, target)

    def show(self):
        return f"min:{self.min} max:{self.max}"


class Solution(MockCf):
    """
    给定一个数组，求最长连续子数组的长度，
    该子数组奇数数量等于偶数数量
    重复元素只计一次
    """

    def longestBalanced(self, nums: List[int]) -> int:
        n = len(nums)
        t = T().set_range(0, n)
        last = dict()
        ans = cur_sum = 0
        for i, x in enumerate(nums, 1):
            v = 1 if x % 2 else -1
            if x not in last:
                cur_sum += v
                t.update(i, n, v)
            else:
                t.update(last[x], i - 1, -v)
            last[x] = i
            j = t.find(0, i - ans - 1, cur_sum)
            if j >= 0:
                ans = i - j
            # self.logger.map(x=x, i=i, j=j, ans=ans, cur_sum=cur_sum)
            # self.logger.info(t)

        return ans

    def longestBalanced(self, nums: List[int]) -> int:
        n = len(nums)
        b = int(math.sqrt(n + 1)) / 2 + 1
        sm = [0] * (n + 1)

        class Node:
            def __init__(self):
                self.l = 0
                self.r = 0

    execute = longestBalanced
