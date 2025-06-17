from common.util.export import List, logger, C


class Solution:
    def get_cases(self):
        return [
            dict(
                n=5,
                nums=[1, 8, 3, 4, 2],
                maxDiff=3,
                queries=[[0, 3], [2, 4]],
                result=[1, 1],
            )
        ]

    def pathExistenceQueries(
        self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]
    ) -> List[int]:
        s = sorted([[v, i] for i, v in enumerate(nums)])
        t = [None] * n
        for j, (_, i) in enumerate(s):
            t[i] = j
        q = [[t[u], t[v]] if t[u] < t[v] else [t[v], t[u]] for u, v in queries]
        r = 1
        p = [-1] * n
        for l in range(n):
            while r < n and s[r][0] - s[l][0] <= maxDiff:
                r += 1
            if r - 1 > l:
                p[l] = r - 1
        logger.map(s=s, t=t, q=q, p=p)
