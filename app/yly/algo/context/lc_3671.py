from common.util.export import List, logger, CT, defaultdict, math


class Solution:
    def get_cases(self):
        return [dict(nums=[1, 2, 3], result=10)]

    def totalBeauty(self, nums: List[int]) -> int:

        n = len(nums)
        g = [{nums[i]: 1} for i in range(n)]
        ans = sum(nums) % CT.MOD
        for i in range(n):
            for j in range(i):
                if nums[j] >= nums[i]:
                    continue
                for k, v in g[j].items():
                    gv = math.gcd(k, nums[i])
                    g[i][gv] = g[i].get(gv, 0) + v
                    ans = (ans + v * gv) % CT.MOD
        return ans

    execute = totalBeauty
