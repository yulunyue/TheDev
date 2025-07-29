from common.util.export import List, Dict, logger, functools


class Solution:
    def get_cases(self):
        return [
            dict(nums=[2, 3, 6, 7], result=15),
            dict(nums=[625, 165, 454, 598], result=1834),
        ]

    def maximizeXorAndXor(self, nums: List[int]) -> int:
        n = len(nums)
        self.mx = 0

        @functools.lru_cache(None)
        def dfs(i, l, m, r):
            if i == n:
                self.mx = max(l + m + r, self.mx)
                return

            dfs(i + 1, l, m, r ^ nums[i])
            dfs(i + 1, l, nums[i] if m == 0 else m & nums[i], r)
            dfs(i + 1, l ^ nums[i], m, r)

        dfs(0, 0, 0, 0)
        return self.mx

    def execute(self, *args, **kw):
        return self.maximizeXorAndXor(*args, **kw)
