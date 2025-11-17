from common.util.export import List, MockCf, inf, CT


class Solution(MockCf):
    def maximumProfit(self, nums: List[int], k: int) -> int:
        f = [[-inf] * 3 for _ in range(k + 2)]
        for j in range(1, k + 2):
            f[j][0] = 0
        for p in nums:
            for j in range(k + 1, 0, -1):
                f[j][0] = CT.max(f[j][0], CT.max(f[j][1] + p, f[j][2] - p))
                f[j][1] = CT.max(f[j][1], f[j - 1][0] - p)
                f[j][2] = CT.max(f[j][2], f[j - 1][0] + p)
        return f[-1][0]

    def maximumScore(self, nums: List[int], k: int) -> int:
        max_i = nums.index(max(nums))
        ans1 = self.maximumProfit(
            nums[max_i:] + nums[:max_i], k
        )  # nums[max_i] 是第一个数
        ans2 = self.maximumProfit(
            nums[max_i + 1 :] + nums[: max_i + 1], k
        )  # nums[max_i] 是最后一个数
        return CT.max(ans1, ans2)

    execute = maximumScore
