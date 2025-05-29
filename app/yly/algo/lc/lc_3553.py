from typing import List
from common.algo.tree import TreeNode


class Solution:
    def get_caces(self):
        return [
            dict(
                edges=[[0, 1, 2], [1, 2, 3], [1, 3, 5], [1, 4, 4], [2, 5, 6]],
                queries=[[2, 3, 4], [0, 2, 5]],
                result=[[2, 3, 4], [0, 2, 5]],
            )
        ]

    def minimumWeight(
        self, edges: List[List[int]], queries: List[List[int]]
    ) -> List[int]:
        g = TreeNode().load_from_edges(edges)
        g.get_dis
