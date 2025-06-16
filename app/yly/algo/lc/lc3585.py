from common.util.export import logger, bisect, List
from common.algo.export import TreeNode


class Solution:
    def get_cases(self):
        return [
            dict(n=2, edges=[[0, 1, 7]], queries=[[1, 0], [0, 1]], result=[0, 1]),
            dict(),
        ]

    def findMedian(self, n, edges, queries):
        nodes = TreeNode.load_from_edges(edges)
        root = nodes[0].set_root().bei_zhen()
        ans = []

        def q(f: TreeNode, mv, chen=0):
            i = bisect.bisect_left(f.path, x=mv, lo=f.depth, key=lambda a: a.path_value)
            ans.append(f.path[i - chen].key)

        for f, t in queries:
            f, t = nodes[f], nodes[t]
            p = root.get_last_lcm_parent(f, t)
            mv = (t.path_value + p.path_value) / 2
            if p.key == f.key:
                q(t, mv, 0)
            elif p.key == t.key:
                q(f, mv, 1)
            else:
                if f.path_value >= t.path_value:
                    q(f, mv, 0)
                else:
                    q(t, mv, 0)
            # logger.map(mv=mv, paths=paths)
        return ans
