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
        self.value = [v, 0, 1, 0]

    def merge(self, lvalue, rvalue):
        ll, lc, ls, lr = lvalue
        rl, rc, rs, rr = rvalue
        mc, ms = lc + rc, ls + rs
        l_full, r_full = ll + lr == ls, rl + rr == rs
        if not l_full and not r_full:
            mm = lr + rl
            mc += (mm + 1) * mm // 2
        elif not l_full and r_full:
            rr = lr + rs
        elif l_full and not r_full:
            ll = ls + rl
        else:
            ll, rr = ms, 0
        return ll, mc, ms, rr


class Solution(MockCf):
    """
    Docstring for Solution
    """

    def get_cases(self):
        return dict(
            case1=dict(
                nums=[3, 1, 2], queries=[[0, 1], [1, 2], [0, 2]], result=[2, 3, 4]
            ),
            case2=dict(nums=[21, 3, 4, 17], queries=[[1, 3]], result=[6]),
            case3=dict(nums=[6, 23, 3, 9], queries=[[0, 3], [1, 2]], result=[6, 2]),
            case4=dict(nums=[20, 24, 31, 33, 16, 41], queries=[[0, 5]], result=[13]),
        )

    def countStableSubarrays(
        self, nums: List[int], queries: List[List[int]]
    ) -> List[int]:
        n = len(nums)
        if n <= 1:
            return [1]
        s = St().set_range(0, n - 2)
        s.build(nums)
        ar = []
        self.logger.info(s)
        for l, r in queries:
            t = r - l + 1
            if l < r:
                lv, vv, size, rv = s.query(l, r - 1)
                t += vv
                t += lv * (lv + 1) // 2
                if lv != size:
                    t += rv * (rv + 1) // 2
                self.logger.map(l=l, r=r - 1, lv=lv, vv=vv, rv=rv)
            ar.append(t)
        return ar

    execute = countStableSubarrays


if __name__ == "__main__":
    Solution().run()
