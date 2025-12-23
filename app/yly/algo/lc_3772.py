from common.util.export import MockCf, List


class Solution(MockCf):
    """
                  A
             /    |   \
          B       C     D
        / | \    / \   / \
       E  F  G  H   I  J  K
    
    给定一颗n个节点的无向树，每个节点的值V要么是1，要么是-1
    求每个节点X的所有连通集的和的最大值S(X), 连通集为包含该节点的子树
    根子树可以为空所以 S(X)>=0 
    
    S(X) = sum([max(S(Y),0) for Y in X])+V(X)
    
    使用换根DP 第一次遍历求得所有的Am, S

 
    
    Fm(B) = S(B) + V(B) + max(0, S(p(B))-Am(B)+V(p(B)))

    """

    def maxSubgraphScore(
        self, n: int, edges: List[List[int]], good: List[int]
    ) -> List[int]:
        g = [[] for _ in range(n)]
        for f, t in edges:
            g[f].append(t)
            g[t].append(f)
        am = [0] * n

        def dfs(u, p):
            am[u] = 1 if good[u] else -1
            for v in g[u]:
                if v == p:
                    continue
                vv = dfs(v, u)
                if vv > 0:
                    am[u] += 1
            return am[u]

        dfs(0, -1)
        f = [0] * n

        def dfs(u, p):
            f[u] = am[u]
            for v in g[u]:
                if v != p:
                    continue
                if am[v] > 0:
                    tmp = am[u] - am[v]
                else:
                    tmp = am[u]
                dfs(v, u)

            return am[u]

        dfs(0, -1)
        return f

    execute = maxSubgraphScore


if __name__ == "__main__":
    Solution().run()
