from common.util.export import List, logger, functools


class Solution:
    def get_cases(self):
        return [
            dict(n=3, edges=[[0, 1], [0, 2]], score=[1, 6, 3], result=25),
            dict(n=2, edges=[[0, 1]], score=[2, 3], result=8),
        ]

    def maxProfit(self, n: int, edges: List[List[int]], score: List[int]) -> int:
        p = [[] for _ in range(n)]
        ps = [0] * n
        vt = [False] * n
        for u, v in edges:
            p[u].append(v)

        def dfs(x, s):
            if vt[x]:
                return
            vt[x] = True
            ps[x] |= s
            s |= 1 << x
            for y in p[x]:
                dfs(y, s)

        for i in range(n):
            dfs(i, 0)

        @functools.lru_cache(None)
        def f(s: int, depth):
            ans = 0
            for i in range(n):
                m = 1 << i
                if s & m:
                    continue
                if s & ps[i] != ps[i]:
                    continue
                v = f(s | m, depth + 1) + depth * score[i]
                ans = max(v, ans)
            return ans

        return f(0, 1)
