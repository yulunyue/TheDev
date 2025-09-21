from common.util.export import List, logger, math


class Solution:
    def get_cases(self):
        return [dict(nums=[1, 2, 3], result=3)]

    def maxXorSubsequences(self, nums: List[int]) -> int:
        mx = max(nums)
        n = mx.bit_length()
        return (1 << n) - 1

    execute = maxXorSubsequences
