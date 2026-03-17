from common.util.export import MockCf, CT, List
from common.algo.base.tree.segtree import SegTreeNode


class T(SegTreeNode):
    def load(self):
        self.value = [0] * self.size

    def merge(self, lv, rv):
        return lv + rv

    def do(self, i, L, R, v, is_inc):

        if is_inc:
            self.value[i] += v * (R - L + 1)
        else:
            self.value[i] *= v
        if L < R:
            if self.todo[i] is None:
                self.todo[i] = [v, is_inc]
            elif self.todo[i][1] == is_inc:
                self.todo[i][0] += v
            elif is_inc:
                self.down(i, L, R)
                self.todo[i] = [v, is_inc]
            else:
                self.todo[i][0] *= v
            self.todo[i][0] %= CT.MOD
        self.value[i] %= CT.MOD


class Fancy:
    def __init__(self, n=10**5):
        self.t = T(n)
        self.idx = -1

    def append(self, val: int) -> None:
        self.idx += 1
        self.t.update(self.idx, self.idx, val, 1)

    def addAll(self, inc: int) -> None:
        if self.idx < 0:
            return
        self.t.update(0, self.idx, inc, 1)

    def multAll(self, m: int) -> None:
        if self.idx < 0:
            return
        self.t.update(0, self.idx, m, 0)

    def getIndex(self, idx: int) -> int:
        if idx > self.idx:
            return -1
        return self.t.query(idx, idx) % CT.MOD


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                req=[
                    "append 2",
                    "append 1",
                    "addAll 2",
                    "getIndex 0",
                    "append 1",
                    "multAll 2",
                    "append 1",
                    "addAll 1",
                    "getIndex 0",
                    "getIndex 1",
                    "getIndex 2",
                    "getIndex 3",
                ],
                result=[4, 9, 7, 3, 2],
            ),
        )

    def execute(self, req: List[str]):
        s = Fancy(5)
        r = []
        for ss in req:
            m, v = ss.split(" ")
            u = getattr(s, m)(int(v))
            if u is not None:
                r.append(u)
            self.logger.map(s=ss, t=s.t.to_str())
        return r
