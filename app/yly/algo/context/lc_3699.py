from common.util.export import functools, CT, logger


class Solution:
    def get_cases(self):
        return [dict(n=3, l=4, r=5, result=2)]

    def zigZagArrays(self, n: int, l: int, r: int) -> int:

        @functools.lru_cache(None)
        def dfs(i, up_down, last_v):
            if i == n:
                return 1
            ans = 0
            for v in range(l, r + 1):
                if v == last_v:
                    continue
                c = 0
                if last_v is None:
                    c = dfs(i + 1, up_down, v)
                elif up_down is None:
                    c = dfs(i + 1, -1 if v < last_v else 1, v)
                elif v > last_v and up_down == -1:
                    c = dfs(i + 1, 1, v)
                elif v < last_v and up_down == 1:
                    c = dfs(i + 1, -1, v)
                ans = (c + ans) % CT.MOD
            # logger.map(i=i, up_down=up_down, last_v=last_v, ans=ans)
            return ans

        ans = dfs(0, None, None)
        dfs.cache_clear()
        return ans

    execute = zigZagArrays
