from common.util.export import List, MockCf, functools


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 2, 3, 1, 2], result=4),
            case1=dict(nums=[2, 2, 2, 2, 2], result=5),
            case2=dict(nums=[4, 0, 5], result=3),
            case3=dict(nums=[1, 4, -2, 7, 9], result=5),
        )

    def longestSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        lt, rt = [1] * n, []
        l = 0
        mn = 0
        idx = []
        for i in range(1, n + 1):
            ct = i - l
            lt[i - 1] = ct
            mn = max(ct + 1, mn)
            if i == n or nums[i] < nums[i - 1]:
                if i + 1 < n and nums[i] <= nums[i + 1]:
                    idx.append(i)
                l = i
        r = n - 1
        for i in range(n - 1, -1, -1):
            v = r - i + 1
            rt.insert(0, v)
            if lt[i] == 1:
                r = i - 1
        self.logger.map(idx=idx, lt=lt, rt=rt)
        for i in idx:
            if nums[i - 1] <= nums[i + 1]:
                mn = max(mn, lt[i - 1] + rt[i + 1] + 1)
            elif i - 2 > 0 and nums[i - 2] <= nums[i]:
                mn = max(mn, lt[i - 1] + rt[i + 1] + 1)
        return min(mn, n)

    execute = longestSubarray
