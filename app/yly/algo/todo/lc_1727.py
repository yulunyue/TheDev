from common.util.export import List, MockCf, CT


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(matrix=[[0, 0, 1], [1, 1, 1], [1, 0, 1]], result=4),
        )

    def largestSubmatrix(self, matrix: List[List[int]]) -> int:
        n, m = len(matrix), len(matrix[0])
        a = 0
        h = [0] * m
        for i in range(n):
            idx = [[], []]
            for j in range(m):
                h[j] = h[j] * matrix[i][j] + matrix[i][j]
                idx[matrix[i][j]].append(j)
            for j, v in enumerate(idx[1]):
                a = CT.max(a, (m - j - len(idx[0])) * h[v])
        return a

    execute = largestSubmatrix
