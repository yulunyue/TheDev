from common.util.export import List, MockCf
from common.algo.base.unifind import UniFind


class Uf(UniFind):
    def __init__(self, n):
        super().__init__(n)
        self.value = [0] * n

    def can_merge(self, child, child_parant, parent, parent_parant, w):
        if child_parant == parent_parant:
            return self.value[child] ^ self.value[parent] == w
        self.value[child_parant] = w ^ self.value[child] ^ self.value[parent]
        return True

    def connect(self, v, p):
        self.value[v] ^= self.value[p]


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case1=dict(n=3, edges=[[0, 1, 1], [1, 2, 1], [0, 2, 1]], expected=2),
            case0=dict(n=3, edges=[[0, 1, 1], [1, 2, 1], [0, 2, 0]], expected=3),
            case2=dict(
                n=4,
                edges=[
                    [0, 1, 0],
                    [1, 2, 0],
                    [2, 3, 1],
                    [0, 2, 0],
                    [0, 3, 0],
                    [1, 3, 0],
                ],
                expected=4,
            ),
        )

    def numberOfEdgesAdded(self, n: int, edges: List[List[int]]) -> int:
        ans = 0
        u = Uf(n)
        for f, t, w in edges:
            ans += u.merge(f, t, w)[1]
            # self.log(f=f, t=t, w=w, ans=ans, u=u.show())
        return ans

    execute = numberOfEdgesAdded
