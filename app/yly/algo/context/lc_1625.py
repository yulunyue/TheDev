from common.util.export import MockCf, functools, defaultdict
from common.algo.base.unifind import UniFind


class Solution(MockCf):
    def findLexSmallestString(self, s: str, a: int, b: int) -> str:
        n = len(s)
        of = [0] * n

        @functools.lru_cache(None)
        def u(v):
            ct = set()
            ret = v
            while v not in ct:
                if v < ret:
                    v = ret
                ct.add(v)
                v += a
            return ret

        for i in range(n):
            pass

    execute = findLexSmallestString
