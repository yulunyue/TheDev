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
                    ret = v
                ct.add(v)
                v = (v + a) % 10
            return ret

        uf = UniFind()
        for i in range(n):
            c = (i + b) % n
            uf.merge(i, c)
            if i % 2 == 1 or c % 2 == 1:
                of[uf.find(i)] = True
        values = defaultdict(list)
        idxs = defaultdict(list)
        for i, v in enumerate(s):
            b = uf.find(i)
            v = int(v)
            if of[b]:
                v = u(v)
            values[b].append(v)
            idxs[b].append(i)

        ret = [""] * n
        for k, vs in values.items():
            for i, v in enumerate(sorted(vs)):
                ret[idxs[k][i]] = str(v)
        return "".join(ret)

    execute = findLexSmallestString
