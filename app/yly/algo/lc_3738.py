from common.util.export import List, MockCf, functools


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 2, 3, 1, 2], result=4),
        )

    def longestSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        lt, rt = dict(), dict()
        l = 0
        mn = 0
        idx = []
        for i in range(1, n):
            if nums[i] < nums[i - 1]:
                ct = i - l
                lt[i - 1] = rt[l] = ct
                mn = max(ct + 1, mn)
                l = i
                if i + 1 < n and nums[i] < nums[i + 1]:
                    idx.append(i)
        for i in idx:
            if nums[i - 1] <= nums[i + 1]:
                mn = max(mn, lt[i - 1] + rt[i + 1] + 1)
            elif i - 2 > 0 and nums[i - 2] <= nums[i]:
                mn = max(mn, lt[i - 1] + rt[i + 1] + 1)
        return mn

    execute = longestSubarray
