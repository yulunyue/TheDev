from common.util.export import defaultdict, C, functools


class Solution:
    def get_cases(self):
        return [dict(n=3, edges=[[0, 1], [1, 2]], label="aba", result=3)]

    def maxLen(self, n, edges, label: str):
        g = defaultdict(list)
        for f, t in edges:
            g[f].append(t)
            g[t].append(f)

        @functools.lru_cache(None)
        def check(l, r, mask):
            if label[l] != label[r]:
                return -C.inf
            if l == r:
                return 1
            max_tmp = 0
            for nl in g[l]:
                lm = 1 << nl
                if lm & mask:
                    continue
                m1 = mask | lm
                for nr in g[r]:
                    rm = 1 << nr
                    if rm & mask:
                        continue
                    m1 |= rm
                    max_tmp = max(max_tmp, check(nl, nr, m1))
            return 2 + max_tmp

        ans = 1
        for i in range(n):
            for j in range(i + 1, n):
                ans = max(ans, check(i, j, (1 << i) + (1 << j)))
        return ans
