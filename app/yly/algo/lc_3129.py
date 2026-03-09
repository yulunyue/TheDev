from common.util.export import List, Dict, MockCf, functools, CT
from common.algo.base.comb import Comb

C = Comb().load(201, CT.MOD)


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case2=dict(zero=1, one=2, limit=1, result=1),
            case1=dict(zero=3, one=3, limit=2, result=14),
            case0=dict(zero=1, one=3, limit=1, result=0),
        )

    def numberOfStableArrays(self, zero: int, one: int, limit: int) -> int:

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
        return e

    execute = numberOfStableArrays
