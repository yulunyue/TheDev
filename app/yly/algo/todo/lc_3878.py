from common.util.export import MockCf, List


class Solution(MockCf):
    """
    给定一个子数组，求子数组的或为子数组的最大值的数量
    随着子数组右端点向右移动，子数组的最大值
    每一位递归找之前的0
    """

    def get_cases(self):
        return dict(
            case1=dict(nums=[1, 2, 3], result=5),
            case0=dict(nums=[6, 10, 4], result=3),
        )

    def countGoodSubarrays(self, nums: list[int]) -> int:
        s = 0
        n = len(nums)
        ans = [0] * n
        ct = dict()
        for i, v in enumerate(nums):

            u, t = 1, v
            for j in range(i - 1, -1, -1):
                vu = v & nums[j]
                if nums[j] < v:
                    u += vu == nums[j]
                    continue
                if vu == v:
                    u += ans[j]
                break
            ct[v] = i
            self.logger.map(u=u)
            ans[i] = u
            s += u
        return s

    execute = countGoodSubarrays
