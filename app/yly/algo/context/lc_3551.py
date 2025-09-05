from common.util.export import functools


class Solution:
    def get_cases(self):
        return [dict(s="01", k=1, result=0)]

    def minOperations(self, s: str, k: int) -> int:
        c = 0
        n = len(s)
        for v in s:
            c += v == "0"
        if 0 < c < k and len(s) == k:
            return -1

        @functools
        def dfs(l):
            r = n - l

            for i in range(-k, k):
                pass

        return dfs(v)
