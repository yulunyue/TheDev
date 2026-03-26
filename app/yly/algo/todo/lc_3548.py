from common.util.export import MockCf, defaultdict, List


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case1=dict(grid=[[1, 4], [2, 3]], result=True),
            case0=dict(grid=[[5, 5, 6, 2, 2, 2]], result=True),
        )

    def canPartitionGrid(self, grid: List[List[int]]) -> bool:
        ct = defaultdict(int)
        s_all = 0
        for row in grid:
            for v in row:
                ct[v] += 1
                s_all += v

        def check(g: List[List[int]]):
            ct1 = defaultdict(int)
            s = 0
            n = len(g)
            for i in range(n - 1):
                row = g[i]
                for v in row:
                    ct1[v] += 1
                    s += v
                c = s - (s_all - s)
                if c == 0:
                    return True
                if c < 0:
                    nm = ct[-c] - ct1[-c]
                    if g[i + 1][0] == -c or g[i + 1][-1] == -c:
                        return True
                    target = 0
                else:
                    nm = ct[c] - ct1[c]
                    if g[i][0] == c or g[i][-1] == c:
                        return True
                    target = n - 2
                if nm and i != target:
                    return True

            return False

        return check(grid) or check(list(zip(*grid)))

    execute = canPartitionGrid
