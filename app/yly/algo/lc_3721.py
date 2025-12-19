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
    https://leetcode.cn/problems/longest-balanced-subarray-ii/description/
    给定一个数组，求最长连续子数组的长度，
    子数组奇数元素数量需要等于偶数数量且重复元素只计一次
    方案一
        使用线段树，记录每个区间的最大值（最多能有多少个偶数）以及最小值（最多能有多少个奇数）
        遍历数组，记录当前的奇偶数差值cur_sum，当前元素的上次出现位置last[x]
        如果当前元素m是个新元素
            那么之后的区间[i,j](i>=m and j<=n)都可以通过包含该元素最大值+1，或者最小值-1。
        否则如果当前元素不是个新元素
            则
    方案二 分块思想
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

    def longestBalanced1(self, nums: List[int]) -> int:
        n = len(nums)
        b_size = int(math.sqrt(n + 1)) / 2 + 1
        sm = [0] * (n + 1)

        class Node:
            def __init__(self, l, r, todo, pos):
                self.l = l  # [l,r) 左闭右开
                self.r = r
                self.todo = todo
                self.pos = pos

        blocks: List[Node] = []

        def cal_pos(l, r):
            pos = dict()
            for j in range(r - 1, l - 1, -1):
                pos[sm[j]] = j
            return pos

        def range_add(l, r, v):
            for i, b in enumerate(blocks):
                if b.r <= l:
                    continue

        def findFirst(r, v):
            pass

        for i in range(0, n + 1, b_size):
            r = min(i + b_size, n + 1)
            pos = cal_pos(i, r)
            blocks.append(Node(i, r, 0, pos))

    execute = longestBalanced
