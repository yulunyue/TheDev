from common.util.export import MockCf, List, defaultdict, functools, CT
from common.algo.base.math_util import prime_gcds, prime_flags

MX = 151
C = prime_gcds(MX)
D = prime_flags(MX)
E = dict()
i = 0
for j, v in enumerate(D):
    if v:
        E[j] = i
        i += 1


@functools.lru_cache(None)
def mask(*args):
    ret = 0
    for a in args:
        ret += 1 << E[a]
    return ret


class Solution(MockCf):
    def countCoprime(self, mat: List[List[int]]) -> int:
        n = len(mat)
        m = len(mat[0])

        @functools.lru_cache(None)
        def dfs(i, p):
            self.logger.map(i=i, p=p)
            if i == n:
                return p == 0
            ans = 0
            for j in range(m):
                mk = mask(*C[mat[i][j]])
                if mat[i][j] == 1 or (mk & p) == 0:
                    ans += pow(m, n - i - 1, CT.MOD)
                else:
                    ans += dfs(i + 1, mk & p)
            return ans % CT.MOD

        return (sum(dfs(1, mask(*C[mat[0][i]])) for i in range(m))) % CT.MOD

    execute = countCoprime
