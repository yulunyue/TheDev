from common.util.export import MockCf, defaultdict, bisect, heapq


class Solution(MockCf):
    def maxRunTime(self, n, nums):
        nums = sorted(nums, reverse=True)
        s = sum(nums)
        for v in nums:
            if n * v <= s:
                return s // n
            s -= v
            n -= 1

    execute = maxRunTime
