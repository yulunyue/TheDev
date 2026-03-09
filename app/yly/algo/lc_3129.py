from common.util.export import List, Dict, MockCf, functools, CT, defaultdict, math
from common.algo.base.comb import Comb

C = Comb().load(201, CT.MOD)


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case2=dict(zero=1, one=2, limit=1, result=1),
            case1=dict(zero=3, one=3, limit=2, result=14),
            case0=dict(zero=1, one=3, limit=1, result=0),
        )

    def numberOfStableArrays_dp(self, zero: int, one: int, limit: int) -> int:

        @functools.lru_cache(None)
        def dfs(i, j, k):
            if i == 0:
                return 1 if j <= limit and k == 1 else 0
            if j == 0:
                return 1 if i <= limit and k == 0 else 0
            if k == 0:
                a = dfs(i - 1, j, 0) + dfs(i - 1, j, 1)
                if i > limit:
                    a -= dfs(i - limit - 1, j, 1)
            else:
                a = dfs(i, j - 1, 0) + dfs(i, j - 1, 1)
                if j > limit:
                    a -= dfs(i, j - limit - 1, 0)
            return a % CT.MOD

        e = dfs(zero, one, 0) + dfs(zero, one, 1)
        dfs.cache_clear()
        return e % CT.MOD

    def numberOfStableArrays(self, zero: int, one: int, limit: int) -> int:
        if zero > one:
            zero, one = one, zero
        f0 = [0] * (zero + 3)

        def u(zero, i):
            r = 0
            for j in range(1, (zero - i) // limit + 1):
                c = -1 if j % 2 else 1
                c *= C.comb(i, j) * C.comb(zero - j * limit - 1, i - 1)
                r = (r + c) % CT.MOD
            return r

        for i in range(math.ceil(zero / limit), zero + 1):
            f0[i] = C.comb(zero - 1, i - 1)
            f0[i] = (f0[i] + u(zero, i)) % CT.MOD
        ans = 0
        for i in range(math.ceil(one / limit), min(one, zero + 1) + 1):
            f1 = C.comb(one - 1, i - 1)
            f1 = f1 + u(one, i)
            ans = (ans + (f0[i - 1] + f0[i] * 2 + f0[i + 1]) * f1) % CT.MOD

        return ans

    execute = numberOfStableArrays
