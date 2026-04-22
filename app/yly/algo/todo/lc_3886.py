from common.util.export import MockCf
from common.algo.base.tree.segtree import SegTreeNode


class T(SegTreeNode):
    pass


class Solution(MockCf):
    """
    给定一个长度为n的整数数组m，对于n的每个因数s
    我们可以将m分成s个子数组t，可以在t内做任意次循环移动使得m非递减
    要使 t 递增，t中有且只能有一个下降，且最小值在最大值右边
    如果 2*t 是满足的
    1<=n<=10**5
    """

    def get_cases(self):
        return dict(case0=dict(nums=[3, 1, 2], result=3))

    def sortableIntegers(self, nums: list[int]) -> int:
        n = len(nums)
        t = T(n - 1, nums)
        for i in range(n):
            if n % i:
                continue
            j = n // i
            for j in range(i + j, n, j):
                t.query()

    execute = sortableIntegers
