from common.util.export import List, Dict, MockCf, functools


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(word="HAPPY", result=6),
        )

    def minimumDistance(self, word: str) -> int:

        def fp(v):
            v = ord(v) - ord("A")
            return v // 6, v % 6

        def d(a, b):
            ay, ax = fp(a)
            by, bx = fp(b)
            return abs(ay - by) + abs(ax - bx)

        @functools.lru_cache(None)
        def dfs(i, la, lb):
            if i == len(word):
                return 0
            lc = word[i]
            v = d(la, lc) + dfs(i + 1, lc, lb)
            if lb is None:
                u = dfs(i + 1, la, lc)
            else:
                u = d(lb, lc) + dfs(i + 1, la, lc)
            return u if u < v else v

        return dfs(1, word[0], None)

    execute = minimumDistance
