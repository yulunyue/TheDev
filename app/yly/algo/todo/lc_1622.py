from common.util.export import MockCf, CT, List
from common.algo.base.tree.segtree import SegTreeNode


class T(SegTreeNode):
    def load(self, *args):
        self.value = 0

    def merge(self, lv, rv):
        return lv + rv

    def do(self, v, f):
        if f == 0:
            self.value = (self.value + v * self.size) % CT.MOD
        else:
            self.value = (self.value * v) % CT.MOD
        if self.size > 1:
            self.down()
            self.todo = [v, f]


class Fancy:
    def __init__(self, n=10**5):
        self.t = T().set_range(0, n).build()
        self.idx = -1

    def append(self, val: int) -> None:
        self.idx += 1
        self.t.update(self.idx, self.idx, val, 0)

    def addAll(self, inc: int) -> None:
        self.t.update(0, self.idx, inc, 0)

    def multAll(self, m: int) -> None:
        self.t.update(0, self.idx, m, 1)

    def getIndex(self, idx: int) -> int:
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
                result=[4],
            ),
        )

    def execute(self, req: List[str]):
        s = Fancy(4)
        r = []
        for ss in req:
            m, v = ss.split(" ")
            u = getattr(s, m)(int(v))
            if u is not None:
                r.append(u)
            self.logger.map(s=ss, t=s.t.to_str())
        return r
