from common.util.export import functools


class Solution:
    def get_cases(self):
        return [dict(n=9, result=6)]

    def countBinaryPalindromes(self, n: int) -> int:
        s = bin(n)[2:]
        n = len(s)
        mid = n // 2
        c1 = [1]
        for i in range(1, n):
            c1.append(c1[i - 1] + (s[i] == "1"))

        @functools.lru_cache(None)
        def dfs(i, uplimit):
            if i == mid:
                return 1
            if uplimit:
                if s[i] == "0":
                    return dfs(i + 1)
                else:
                    if s[n - i - 1] == "1":
                        return 2 * dfs(i + 1, uplimit)
                    else:
                        c = c1[n - 1] - c[i]
                        if c > 0:
                            return 2 ** (mid - i) // 2
                        return 0
            return 0

        return dfs(0, True) + 1

    execute = countBinaryPalindromes
