from common.util.export import List, MockCf, CT


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                matrix=[[0, 0, 1], [1, 1, 1], [1, 0, 1]],
                result=4,
            ),
            case1=dict(
                matrix=[[1, 1, 0], [1, 0, 1]],
                result=2,
            ),
        )

    def largestSubmatrix(self, matrix: List[List[int]]) -> int:
        n, m = len(matrix), len(matrix[0])
        a = 0
        h = [0] * m
        ix = range(m)
        for i in range(n):
            idx = [[], []]
            for j in range(m):
                if matrix[i][j] == 0:
                    h[j] = 0
                else:
                    h[j] += 1
                idx[matrix[i][j]].append(ix[j])
            ix = idx[0] + idx[1]
            for j, v in enumerate(idx[1]):
                a = CT.max(a, (m - j - len(idx[0])) * h[v])
        return a

    execute = largestSubmatrix
