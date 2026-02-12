from common.util.export import MockCf
from common.algo.base.block import Block


class Solution:
    def get_cases(self):
        return dict(nums=[2, 5, 4, 3], result=4)

    def longestBalanced(self, nums: List[int]) -> int:
        n = len(nums)
        bs = Block(n)
        last_idx = dict()
        for i, v in enumerate(nums):
            u = 1 if v % 2 else -1
            bs.add(i, n - 1, u)
            last_idx[v] = i
