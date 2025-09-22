from common.util.export import List, logger, math
from common.algo.base.xor_basis import XorBais


class Solution:
    def get_cases(self):
        return [dict(nums=[1, 2, 3], result=3)]

    def maxXorSubsequences(self, nums: List[int]) -> int:
        x = XorBais().set_b(nums)
        return x.max_xor()

    execute = maxXorSubsequences
