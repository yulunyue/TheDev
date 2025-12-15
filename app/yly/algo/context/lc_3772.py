from common.util.export import MockCf, List


class Solution(MockCf):
    """
                  A
             /    |   \
          B       C     D
        / | \    / \   / \
       E  F  G  H   I  J  K
    
    给定一颗n个节点的无向树，每个节点的值V要么是1，要么是-1
    求每个节点的所有连通集的和的最小值Fm, 连通集为包含该节点的子树
    定义根子树和的最小值为函数Am Am>=0
    S(X)=sum(Am(X...)    
    Fm(A)=S(A)+V(A)
    Fm(B)=S(B)+V(B)+max(Fm(A)-max(S(B)+V(B),0),0)
    """

    def maxSubgraphScore(
        self, n: int, edges: List[List[int]], good: List[int]
    ) -> List[int]:
        pass

    execute = maxSubgraphScore
