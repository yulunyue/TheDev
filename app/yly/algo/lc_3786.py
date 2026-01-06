from common.util.export import MockCf, List, defaultdict


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                n=4, edges=[[0, 1], [0, 2], [0, 3]], group=[1, 1, 4, 4], result=3
            ),
            case1=dict(n=3, edges=[[0, 1], [1, 2]], group=[1, 1, 1], result=4),
        )

    def interactionCosts(self, n: int, edges: List[List[int]], group: List[int]) -> int:
        M = 20
        g: List[List[int]] = [[] for _ in range(n)]
        for f, t in edges:
            g[f].append(t)
            g[t].append(f)
        self.ans = 0

        sm: List[dict] = [[[0, 0] for _ in range(M)] for _ in range(n)]

        def dfs(v, p, d=0):
            for u in g[v]:
                if u == p:
                    continue
                dfs(u, v, d + 1)
                for i, c in enumerate(sm[u]):
                    sm[v][i][0] += c[0]
                    sm[v][i][1] += c[1]
            sm[v][group[v]][0] += 1
            sm[v][group[v]][1] += d

        dfs(0, -1)
        self.ans = 0
        # self.logger.log_tree(g, lambda v: sm[v][group[v]])

        def dfs(v, p):
            # self.logger.log_tree(g, lambda v: str(dict(sm[v])))
            if p != -1:
                for i in range(M):
                    vv, pp = sm[v][i], sm[p][i]
                    vv[1] += sm[0][i][0] - vv[0] + pp[1] - vv[1] - vv[0]
            self.ans += sm[v][group[v]][1]
            # self.logger.map(v=v, ans=self.ans, u=sm[v][group[v]])

            for u in g[v]:
                if u == p:
                    continue
                dfs(u, v)

        dfs(0, -1)
        return self.ans // 2

    execute = interactionCosts


if __name__ == "__main__":
    Solution().run()
