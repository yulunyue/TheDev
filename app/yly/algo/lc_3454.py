from common.util.export import MockCf, List, defaultdict, bisect
from common.algo.base.segtree import SegTreeNode


class T(SegTreeNode):

    def load(self, nums: List[int]):
        self.value = [0, nums[self.l + 1] - nums[self.l]]

    def do(self, v):
        self.todo += v
        self.value[0] += v

    def merge(self, l, r):
        mn = min(l[0], r[0])
        ln = 0
        if mn == l[0]:
            ln += l[1]
        if mn == r[0]:
            ln += r[1]
        return [mn, ln]


class T(SegTreeNode):
    def __init__(self, idx=1):
        super().__init__(idx)
        self.value = [0, 0, 0]

    def load(self, nums: List[int]):
        self.value[2] = nums[self.l + 1] - nums[self.l]

    def do(self, v):
        self.value[0] += v
        self.up()

    def up(self):
        if self.l != self.r:
            self.value[2] = self.left.value[2] + self.right.value[2]
        if self.value[0] > 0:
            self.value[1] = self.value[2]
        elif self.l != self.r:
            self.value[1] = self.left.value[1] + self.right.value[1]
        else:
            self.value[1] = 0


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(squares=[[0, 0, 1], [2, 2, 1]], result=1.00000),
            case1=dict(squares=[[0, 0, 2], [4, 0, 3]], result=1.3),
            case2=dict(squares=[[0, 3, 3], [2, 0, 5]], result=3.14286),
            case4=dict(squares=[[12, 14, 7], [8, 12, 6]], result=16.40909),
        )

    def separateSquares(self, squares: List[List[int]]) -> float:
        c = defaultdict(list)
        s = set()
        for x, y, l in squares:
            r = x + l
            c[y].append([x, r, 1])
            c[y + l].append([x, r, -1])
            s.update([x, r])
        s = sorted(s)
        ct = dict()
        for i, v in enumerate(s):
            ct[v] = i
        t = T().set_range(0, len(s) - 2).build(s)
        sa = [[0]]
        lx = None
        # self.logger.info(s)
        self.logger.info(t)
        for y in sorted(c.keys()):
            for cy in c[y]:
                l, r, v = ct[cy[0]], ct[cy[1]] - 1, cy[2]
                t.update(l, r, v)
                # self.logger.map(l=l, r=r, v=v)
            self.logger.info(t)
            if lx:
                sa.append([sa[-1][0] + lx * (y - ly), y * 1.0, lx])
            # self.logger.map(lx=lx, y=y)
            xx = t.query(0, len(s) - 1)
            # lx, ly = s[-1] - s[0] - (0 if xx[0] else xx[1]), y
            lx, ly = xx[1], y

        mid = sa[-1][0] / 2
        idx = bisect.bisect_left(sa, [mid])
        # self.logger.map(sa=sa, idx=idx, md=mid)
        return sa[idx][1] + (mid - sa[idx][0]) / sa[idx][2]

    execute = separateSquares


if __name__ == "__main__":
    Solution().run()
