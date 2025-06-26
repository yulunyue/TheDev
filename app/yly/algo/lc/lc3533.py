from common.util.export import List, functools


class Solution:
    def get_cases(self):
        return [dict(nums=[12, 3, 45], k=5, result=[3, 12, 45])]

    def concatenatedDivisibility(self, nums: List[int], k: int) -> List[int]:
        nums.sort()
        n = len(nums)
        chen = [10 ** len(str(v)) for v in nums]
        ans = []

        @functools.lru_cache(None)
        def dfs(m, v):
            if m == (1 << n) - 1:
                return v == 0
            for i in range(n):
                mi = 1 << i
                if m & mi:
                    continue
                v1 = (v + nums[i] * chen[i]) % k
                if dfs(m | mi, v1):
                    ans.append(nums[i])
                    return True
            return False

        if not dfs(0, 0):
            return []
        ans.reverse()
        return ans
