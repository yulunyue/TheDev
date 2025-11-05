from common.util.export import MockCf, List, defaultdict, functools, CT, math
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


MX = 151
divisors = [[] for _ in range(MX)]
for i in range(1, MX):
    for j in range(i, MX, i):
        divisors[j].append(i)


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

    def countCoprime(self, mat: List[List[int]]) -> int:
        MOD = 1_000_000_007

        @functools.lru_cache(None)  # 缓存装饰器，避免重复计算 dfs（一行代码实现记忆化）
        def dfs(i: int, g: int) -> int:
            if i < 0:
                return 1 if g == 1 else 0
            return sum(dfs(i - 1, math.gcd(g, x)) for x in mat[i]) % MOD

        return dfs(len(mat) - 1, 0)

    def countCoprime(self, mat: List[List[int]]) -> int:
        MOD = 1_000_000_007
        # 预处理每行的因子个数
        divisor_cnt = []
        mx = 0
        for row in mat:
            row_max = max(row)
            mx = max(mx, row_max)
            cnt = [0] * (row_max + 1)
            for x in row:
                for d in divisors[x]:
                    cnt[d] += 1
            divisor_cnt.append(cnt)

        cnt_gcd = [0] * (mx + 1)
        for i in range(mx, 0, -1):
            # 每行选一个 i 的倍数的方案数
            res = 1
            for cnt in divisor_cnt:
                if i >= len(cnt) or cnt[i] == 0:
                    res = 0
                    break
                res = res * cnt[i] % MOD  # 乘法原理

            for j in range(i, mx + 1, i):
                res -= cnt_gcd[j]
            cnt_gcd[i] = res % MOD

        return cnt_gcd[1]

    execute = countCoprime
