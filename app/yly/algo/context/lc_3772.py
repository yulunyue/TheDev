from common.util.export import MockCf, List


class Solution(MockCf):
    """
                  A
             /    |   \
          B       C     D
        / | \    / \   / \
       E  F  G  H   I  J  K
    
    给定一颗n个节点的无向树，每个节点的值V要么是1，要么是-1
    求每个节点的所有连通集的和Fm的最小值，  连通集为包含该节点的子树
    定义子树的和为函数F
    以A为根jid
    """

    def maxSubgraphScore(
        self, n: int, edges: List[List[int]], good: List[int]
    ) -> List[int]:
        pass

    execute = maxSubgraphScore
