from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                n=7,
                edges=[[0, 1], [1, 2], [2, 3], [3, 4], [3, 5], [1, 6]],
                start="0011000",
                target="0010001",
                result=[1, 2, 5],
            ),
            case1=dict(
                n=2,
                edges=[[0, 1]],
                start="00",
                target="01",
                result=[-1],
            ),
        )

    def minimumFlips(
        self, n: int, edges: List[List[int]], start: str, target: str
    ) -> List[int]:
        g = [[] for _ in range(n)]
        vs = [0 if start[i] == target[i] else 1 for i in range(n)]
        for i, (f, t) in enumerate(edges):
            g[f].append([t, i])
            g[t].append([f, i])
        ans = []

        def dfs(u, p=-1):
            cc = 0
            for v, i in g[u]:
                if v == p:
                    continue
                c = dfs(v, u)
                if c == 1:
                    ans.append(i)
                cc += c
            return 0 if cc % 2 == vs[u] else 1

        return sorted(ans) if dfs(0) == 0 else [-1]

    execute = minimumFlips
