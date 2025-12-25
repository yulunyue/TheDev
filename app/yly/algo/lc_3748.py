"""
给定一个数组 nums
查询数组q
要求对于q中的每一个l,r
nums[l,r+1]中有效子数组(任意两个相邻元素非递减)的数量
线段树合并
"""

from common.util.export import List, MockCf
from common.algo.base.segtree import SegTreeNode


class St(SegTreeNode):
    def init(self, nums):
        v = 1 if nums[self.l] <= nums[self.l + 1] else 0
        self.value = [v, 0, v]

    def merge(self, lvalue, rvalue):
        l1, l2, l3 = lvalue
        r1, r2, r3 = rvalue
        if l3 == self.left.size:
            return l3 + r1, r2, r3
        if r1 == self.right.size:
            return l1, l2, l3 + r1
        v = l2 + r2
        v += (l3 + r1) * (l3 + r1 + 1) // 2
        return l1, v, r3


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case1=dict(
                nums=[3, 1, 2], queries=[[0, 1], [1, 2], [0, 2]], result=[2, 3, 4]
            )
        )

    def countStableSubarrays(
        self, nums: List[int], queries: List[List[int]]
    ) -> List[int]:
        n = len(nums)
        s = St().set_range(0, n - 2)
        s.build(nums)
        ar = []
        for l, r in queries:
            if l == r:
                ar.append(1)
            else:
                lv, vv, rv = s.query(l, r)

                ar.append(vv + r - l + 1 + lv * (lv + 1) // 2 + rv * (rv + 1) // 2)
        return ar

    execute = countStableSubarrays


if __name__ == "__main__":
    Solution().run()
