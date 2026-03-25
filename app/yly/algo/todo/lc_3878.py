from common.util.export import MockCf, List, functools


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
        n = len(nums)
        mx = max(nums)
        mx_or = (1 << mx.bit_length()) - 1

        @functools.lru_cache(None)
        def dfs(i, v):
            if i < 0:
                return 0
            v_or = nums[i] | v
            if v_or == v or v_or == nums[i]:
                return 1 + dfs(i - 1, v_or)
            if v_or == mx_or:
                return i + 1
            r = dfs(i - 1, v_or)
            # self.logger.map(i=i, v=v, r=r)
            return r

        return sum([dfs(i, 0) for i in range(1, n)])

    execute = countGoodSubarrays
