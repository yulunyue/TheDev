from common.util.export import MockCf, List, defaultdict, functools, math
from common.algo.base.math_util import prime_flags

MX = MV = 10**5 + 1
FGS = prime_flags(MV)
FLG = [i for i, v in enumerate(FGS) if v]
core = [0] * MX
for i in range(1, MX):
    if core[i] == 0:
        for j in range(1, math.isqrt(MX // i) + 1):
            core[i * j * j] = i


class Solution(MockCf):
    def sumOfAncestors(self, n: int, edges: List[List[int]], nums: List[int]) -> int:
        g = defaultdict(list)
        for f, t in edges:
            g[f].append(t)
            g[t].append(f)

        @functools.lru_cache(None)
        def find(t):
            if FGS[t]:
                return t
            a, s = 1, t
            idx = 0
            while s > 1 and FLG[idx] <= s:
                if s % FLG[idx]:
                    idx += 1
                    continue
                if a % FLG[idx] == 0:
                    a = a // FLG[idx]
                else:
                    a = a * FLG[idx]
                s = s // FLG[idx]
            return a

        self.ans = 0
        self.ct = defaultdict(int)

        def dfs(v, p=-1):
            d = find(nums[v])  # core[nums[v]]
            self.ans += self.ct[d]
            self.ct[d] += 1
            for u in g[v]:
                if u == p:
                    continue
                dfs(u, v)
            self.ct[d] -= 1

        dfs(0)
        return self.ans

    execute = sumOfAncestors
