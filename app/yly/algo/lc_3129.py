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
        z, o, l = zero, one, limit
        a = z + o
        # b = C.comb(a, z)
        d = 0

        @functools.lru_cache(None)
        def dfs(i, c, e, z, o):
            if i == a or z < 0 or o < 0 or c > l or e > l:
                ret = 0
            elif c + z <= l and e + o <= l:
                self.logger.map(i=i, c0=c, r0=z, c1=e, r1=o)
                ret = C.comb(a - i, z)
            else:
                ret = dfs(i + 1, c + 1, 0, z - 1, o) + dfs(i + 1, 0, e + 1, z, o - 1)

            return ret % CT.MOD

        e = dfs(0, 0, 0, z, o)
        dfs.cache_clear()
        return e

    execute = numberOfStableArrays
