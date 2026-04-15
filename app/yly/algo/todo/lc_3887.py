from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(n=3, edges=[[0, 1, 1], [1, 2, 1], [0, 2, 1]], result=2),
        )

    def numberOfEdgesAdded(self, n: int, edges: List[List[int]]) -> int:
        pass

    execute = numberOfEdgesAdded
