from common.util.export import MockCf, List, defaultdict, bisect
from common.algo.base.segtree import SegTreeNode


class T(SegTreeNode):
    value = 0

    def do(self, v):
        self.todo += v
        self.min_cover += v


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(squares=[[0, 0, 1], [2, 2, 1]], result=1.00000),
            case1=dict(squares=[[0, 0, 2], [4, 0, 3]], result=1.3),
            case2=dict(squares=[[0, 3, 3], [2, 0, 5]], result=3.14286),
        )

    def separateSquares(self, squares: List[List[int]]) -> float:
        c = defaultdict(list)
        mx = 0
        for x, y, l in squares:
            c[y].append([x, x + l - 1, 1])
            c[y + l].append([x, x + l - 1, -1])
            mx = max(mx, x + l - 1)
        t = T().set_range(0, mx)
        sa = [[0]]
        lx = None
        for y in sorted(c.keys()):
            for cy in c[y]:
                t.update(*cy)
                self.logger.info(cy)
            self.logger.info(t.str_view())
            if lx:
                sa.append([sa[-1][0] + lx * (y - ly), y * 1.0, lx])
                self.logger.map(lx=lx, y=y, yc=y - ly)
            lx, ly = t.query(0, mx), y

        mid = sa[-1][0] / 2
        idx = bisect.bisect_left(sa, [mid])
        # self.logger.map(sa=sa, idx=idx, md=mid)
        return sa[idx][1] + (mid - sa[idx][0]) / sa[idx][2]

    execute = separateSquares


if __name__ == "__main__":
    Solution().run()
