from typing import List
from common.algo.base.tree import TreeNode


class Solution:
    def get_caces(self):
        return [
            dict(
                edges=[[0, 1, 2], [1, 2, 3], [1, 3, 5], [1, 4, 4], [2, 5, 6]],
                queries=[[2, 3, 4], [0, 2, 5]],
                result=[12, 11],
            )
        ]

    def minimumWeight(
        self, edges: List[List[int]], queries: List[List[int]]
    ) -> List[int]:
        nodes = TreeNode.load_from_edges(edges)
        root = nodes[0].bei_zhen()
        ret = []
        for f, t, r in queries:
            a = (
                root.get_dis2node(nodes[f], nodes[t])
                + root.get_dis2node(nodes[t], nodes[r])
                + root.get_dis2node(nodes[f], nodes[r])
            ) // 2
            ret.append(a)
        return ret
