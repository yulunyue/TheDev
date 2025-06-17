from common.util.export import logger, bisect, List
from common.algo.export import TreeNode


class Solution:
    def get_cases(self):
        return [
            dict(n=2, edges=[[0, 1, 7]], queries=[[1, 0], [0, 1]], result=[0, 1]),
            dict(
                n=5,
                edges=[[0, 1, 2], [0, 2, 5], [1, 3, 1], [2, 4, 3]],
                queries=[[3, 4], [1, 2]],
                result=[2, 2],
            ),
        ]

    def findMedian(self, n, edges, queries):
        nodes = TreeNode.load_from_edges(edges)
        root = nodes[0].set_root().bei_zhen()
        ans = []

        def q(f: TreeNode, mv, lo, chen=0):
            # logger.map(mv=mv, paths=f.path, chen=chen)
            i = bisect.bisect_left(f.path, x=mv, lo=lo, key=lambda a: a.path_value)
            ans.append(f.path[i - chen].key)

        for f, t in queries:
            f, t = nodes[f], nodes[t]
            p = root.get_last_lcm_parent(f, t)
            mv = (t.path_value + f.path_value) / 2
            if p.key == f.key:
                q(t, mv, p.depth, 0)
            elif p.key == t.key:
                q(f, mv, p.depth, 1)
            else:
                if f.path_value >= t.path_value:
                    q(f, mv - t.path_value, p.depth, 0)
                else:
                    q(t, mv - f.path_value, p.depth, 0)

        return ans
