from common.util.export import List, SortedSet, defaultdict


class Solution:
    def get_cases(self):
        return [
            dict(
                par=[-1, 0, 0],
                vals=[1, 1, 1],
                queries=[[0, 1], [0, 2], [0, 3]],
                result=[0, 1, -1],
            )
        ]

    def kthSmallest(
        self, par: List[int], vals: List[int], queries: List[List[int]]
    ) -> List[int]:
        n, m = len(par), len(queries)
        ans = [-1] * m
        q = defaultdict(list)
        for i, (idx, k) in enumerate(queries):
            q[idx].append([k, i])
        g = [[] for _ in range(n)]
        for i, v in enumerate(par):
            if v == -1:
                continue
            g[v].append(i)

        def dfs(i, x):
            x ^= vals[i]
            s = SortedSet([x])
            for j in g[i]:
                s1 = dfs(j, x)
                if len(s1) > len(s):
                    s, s1 = s1, s
                for v in s1:
                    s.add(v)
            for k, j in q[i]:
                if k - 1 < len(s):
                    ans[j] = s[k - 1]
            return s

        dfs(0, 0)
        return ans
