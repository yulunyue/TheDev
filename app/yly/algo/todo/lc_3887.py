from common.util.export import List, MockCf
from common.algo.base.unifind import UniFind

class Uf(UniFind):
    def __init__(self, n):
        super().__init__(n)
        self.value=[0]*n
    def can_merge(self, child, child_parant, parent, parent_parant, w):
        d = self.value[parent_parant]+self.value[child_parant]+w
        if child_parant==parent_parant and (d+w)%2==1:
            return False
        self.value[parent_parant],self.value[child_parant]=d,0
        return super().can_merge(child, child_parant, parent, parent_parant, w)

class Solution(MockCf):
    def get_cases(self):
        return dict(
            case1=dict(n=3, edges=[[0, 1, 1], [1, 2, 1], [0, 2, 1]], result=2),
            case0=dict( n = 3, edges = [[0,1,1],[1,2,1],[0,2,0]],result=3)
        )

    def numberOfEdgesAdded(self, n: int, edges: List[List[int]]) -> int:
        ans=0
        u=Uf(n)
        for f,t,w in edges:
            ans+=u.merge(f,t,w)[1]
            # self.log(ans=ans,u=u.show())
        return ans
            

    execute = numberOfEdgesAdded
