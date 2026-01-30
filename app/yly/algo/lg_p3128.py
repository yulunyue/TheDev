from common.util.export import MockCf, Dict, List, defaultdict
from common.algo.base.tree.beizhen_tree import Tree


class Solution(MockCf):
    S1 = """5 10
3 4
1 5
4 2
5 4
5 4
5 4
3 5
4 3
4 3
1 3
3 5
5 4
1 5
3 4"""
    uri = """
    https://www.luogu.com.cn/problem/P3128
    """

    def get_cases(self):
        return dict(case0=dict(inps=self.S1, result="9"))

    def main(self):
        n, k = self.ii()
        edges = [self.ii() for _ in range(n - 1)]
        nodes: Dict[int, Tree] = Tree.load_from_edges(edges)
        root = nodes[1].bei_zhen()
        # self.logger.log_tree(root.to_json())
        for _ in range(k):
            s1, e1 = self.ii()
            s, e = nodes[s1], nodes[e1]
            s.value += 1
            e.value += 1
            p = root.get_last_lcm_parent(s, e)
            p.value -= 1
            if p != root:
                pp = root.get_k_parent(p, 1)
                pp.value -= 1
            # self.logger.log_tree(root.to_json())

        self.ans = 0

        def dfs(r: Tree, p=None):
            v = r.value
            for d in r.out_edges.values():
                if d.dst != p:
                    v += dfs(d.dst, r)
            if v > self.ans:
                self.ans = v
            return v

        dfs(root)
        return self.ans


if __name__ == "__main__":
    print(Solution().main())
