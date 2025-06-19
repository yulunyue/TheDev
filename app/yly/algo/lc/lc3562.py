from common.util.export import List, logger, defaultdict


class Solution:
    def get_cases(self):
        return [
            dict(
                n=2,
                present=[1, 2],
                future=[4, 3],
                hierarchy=[[1, 2]],
                budget=3,
                result=5,
            )
        ]

    def maxProfit(
        self,
        n: int,
        present: List[int],
        future: List[int],
        hierarchy: List[List[int]],
        budget: int,
    ) -> int:
        g = [[] for _ in range(n)]
        for x, y in hierarchy:
            g[x - 1].append(y - 1)

        def dfs(i):
            ct = [defaultdict(int), defaultdict(int)]
            for j in g[i]:
                jt = dfs(j)
            for i, c in enumerate(ct):
                p = present[x] // (i + 1)
            return ct

        return max(dfs(0)[0].values())
