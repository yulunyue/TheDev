from common.util.export import functools, logger


class Solution:
    def get_cases(self):
        return [
            dict(s="bcda", result=""),
            dict(s="abc", result="a"),
            dict(s="zdce", result="zdce"),
        ]

    def lexicographicallySmallestString(self, s: str) -> str:
        def check(a, b):
            c = abs(ord(a) - ord(b))
            return c == 1 or c == 25

        n = len(s)

        @functools.lru_cache(None)
        def can_clear(l, r):
            if l > r:
                return True
            for k in range(l + 1, r + 1, 2):
                if (
                    check(s[l], s[k])
                    and can_clear(l + 1, k - 1)
                    and can_clear(k + 1, r)
                ):
                    # logger.map(s=s[l : r + 1], f=1)
                    return True
            # logger.map(s=s[l : r + 1], f=0)
            return False

        @functools.lru_cache(None)
        def dfs(i):
            if i >= n:
                return ""
            res = s[i] + dfs(i + 1)
            for j in range(i + 1, n, 2):
                if can_clear(i, j):
                    res = min(res, dfs(j + 1))
            # logger.map(i=i, res=res)
            return res

        return dfs(0)
