from common.util.export import MockCf, heapq, CT, List
from common.algo.base.unifind import UniFind


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(n=3, edges=[[0, 1, 2, 1], [1, 2, 3, 0]], k=1, result=2),
        )

    def maxStability(self, n: int, edges: List[List[int]], k: int) -> int:
        ufm = UniFind(n)
        mn = CT.inf
        h = []
        for f, t, w, m in edges:
            if m:
                if not ufm.merge(f, t)[1]:
                    return -1
                mn = CT.min(mn, w)
            else:
                heapq.heappush(h, [w, f, t])
        if ufm.size == n - 1:
            return mn
        d = []
        while h and ufm.size < n - 1:
            w, f, t = heapq.heappop(h)
            if ufm.merge(f, t)[1]:
                d.append(w)
        mn = CT.min(mn, d[0] * 2)
        self.logger.map(mn=mn, d=d)
        if k <= len(d):
            return CT.min(mn, d[k - 1])
        return mn

    execute = maxStability
