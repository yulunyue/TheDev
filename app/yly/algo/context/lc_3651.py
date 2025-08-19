from common.util.export import List, functools, CT, defaultdict, logger


class Solution:
    def get_cases(self):
        return [dict(grid=[[1, 3, 3], [2, 5, 4], [4, 3, 5]], k=2, result=7)]

    def minCost(self, grid: List[List[int]], k: int) -> int:
        self.n, self.m = len(grid), len(grid[0])

        max_v = max(map(max, grid))
        self.lm = [CT.inf] * (max_v + 2)

        for u in range(k + 1):
            ct = defaultdict(lambda: CT.inf)
            ct[0, 0] = 0
            mx_v = [CT.inf] * (max_v + 1)
            for i, row in enumerate(grid):
                for j, v in enumerate(row):
                    if i == 0 and j == 0:
                        continue
                    mv = CT.min(ct[i, j - 1], ct[i - 1, j])
                    ct[i, j] = min(mv + v, ct[i, j], self.lm[v])
                    mx_v[v] = CT.min(mx_v[v], ct[i, j])
            for v in range(max_v, -1, -1):
                self.lm[v] = CT.min(self.lm[v + 1], mx_v[v])
        return ct[self.n - 1, self.m - 1]

    def log(self, tmp, k=None):
        ret = []
        for i in range(self.n):
            s = []
            for j in range(self.m):
                if k is not None:
                    s.append(str(tmp[k, i, j]))
                else:
                    s.append(str(tmp[i][j]))
            ret.append(",".join(s))
        s2 = "\n".join(ret)
        logger.debug(f"\n-----{k}-----\n{s2}\n{self.lm}")

    def execute(self, **kw):
        return self.minCost(**kw)
