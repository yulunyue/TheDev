from common.util.export import List, functools


class Solution:
    def minMoves(self, nums: List[int], limit: int) -> int:
        n = len(nums)

        @functools.lru_cache(None)
        def dfs():
            pass

        return dfs(n - 1)
