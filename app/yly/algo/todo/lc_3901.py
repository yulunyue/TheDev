from common.util.export import List, MockCf, CT, defaultdict, math

from common.algo.base.tree.segtree import SegTreeNode


class SegTree(SegTreeNode):
    def load(self, nums, p):
        self.nums = nums
        self.p = p
        self.value = [0] * self.size
        self.build(1, 0, self.n)

    def do(self, i, L, R, *v):
        self.value[i] = self.nums[L] if self.nums[L] % self.p == 0 else 0

    def merge(self, l, r):
        return math.gcd(l, r)

    def query(self, l, r):
        if l > r:
            return 0
        return super().query(l, r)

    def check(self):

        return any(
            math.gcd(self.query(0, i - 1), self.query(i + 1, self.n)) == self.p
            for i in range(self.n + 1)
        )


class Solution(MockCf):
    """
    对于
    """

    def get_cases(self):
        return dict(
            case0=dict(nums=[4, 8, 12, 16], p=2, queries=[[0, 3], [2, 6]], result=1),
            case1=dict(
                nums=[4, 5, 7, 8], p=3, queries=[[0, 6], [1, 9], [2, 3]], result=2
            ),
            case2=dict(
                nums=[1, 5, 56, 22, 49, 18, 27, 69],
                p=19,
                queries=[[0, 9], [0, 15], [6, 23]],
                result=0,
            ),
            case4=dict(
                nums=[1, 6],
                p=7,
                queries=[[0, 7]],
                result=1,
            ),
            case3=dict(
                nums=[2, 3],
                p=1,
                queries=[[0, 4], [1, 6]],
                result=0,
            ),
            case5=dict(nums=[9, 13, 5], p=1, queries=[[1, 10]], result=1),
            case6=dict(
                nums=[
                    356,
                    179,
                    353,
                    210,
                    329,
                    130,
                    153,
                    301,
                    348,
                    272,
                    270,
                    8,
                    252,
                    344,
                    110,
                    53,
                    53,
                    344,
                    94,
                ],
                p=18,
                queries=[[11, 54], [9, 283], [11, 278], [5, 35], [10, 285], [7, 69]],
                result=4,
            ),
        )

    def countGoodSubseq(self, nums: list[int], p: int, queries: list[list[int]]) -> int:
        n = len(nums)
        cnt_p = sum(x % p == 0 for x in nums)
        t = SegTree(n - 1, nums, p)
        ans = 0
        for i, x in queries:
            cnt_p += (x % p == 0) - (nums[i] % p) == 0
            nums[i] = x
            t.update(i, i, x)

            if t.value[1] == p:
                if cnt_p < n or n > 6 or t.check():
                    ans += 1
            # self.log(nums=nums, p=p, ans=ans, t=t.to_str())

        return ans

    execute = countGoodSubseq
