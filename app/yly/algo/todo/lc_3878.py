from common.util.export import MockCf, List


class Solution(MockCf):
    """
    给定一个子数组，求子数组的或为子数组的最大值的数量
    随着子数组右端点向右移动，子数组的最大值
    """

    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 2, 3], result=5),
        )

    def countGoodSubarrays(self, nums: list[int]) -> int:
        s = 0
        n = len(nums)
        ans = [0] * n
        for i, v in enumerate(nums):
            u = 1
            for j in range(i - 1, -1, -1):
                vu = v & nums[j]
                if nums[j] < v:
                    u += vu == nums[j]
                elif vu == v:
                    u += ans[j]
                    break
            ans[i] = u
            s += u
        return s

    execute = countGoodSubarrays
