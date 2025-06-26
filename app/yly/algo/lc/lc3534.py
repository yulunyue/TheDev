from common.util.export import List, logger, C
from common.algo.base.math_util import bei_zen


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
        l = 0
        p = []
        for r in range(n):
            while s[r][0] - s[l][0] > maxDiff:
                l += 1
            p.append(l)
        pa = bei_zen(p)
        ans = []
        for l, r in q:
            pass
        # logger.map(s=s, q=q, p=p)
        return ans
