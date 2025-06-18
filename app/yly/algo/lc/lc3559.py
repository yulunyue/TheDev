from common.util.export import List, logger, math
from common.algo.base.tree import TreeNode


class Solution:
    def get_cases(self):
        return [
            dict(
                edges=[[1, 2], [1, 3], [3, 4], [3, 5]],
                queries=[[1, 4], [3, 4], [2, 5]],
                result=[2, 1, 4],
            )
        ]

    def assignEdgeWeights(
        self, edges: List[List[int]], queries: List[List[int]]
    ) -> List[int]:
        nodes = TreeNode.load_from_edges(edges)
        root = nodes[1].bei_zhen()
        ans = []
        for f, t in queries:
            if f == t:
                ans.append(0)
                continue
            n = root.get_dis2node(nodes[f], nodes[t])
            ans.append(2 ** (n - 1))
        return ans
