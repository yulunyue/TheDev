from common.algo.base.tree.segtree import SegTreeNode


class T(SegTreeNode):
    def load(self):
        self.value = 0

    def do(self, v, tp):
        self.todo = [v, tp]
        if tp == 0:
            self.value += tp
        else:
            self.value *= tp


class Fancy:

    def __init__(self):
        self.s: T = T().set_range(0, (10**5) + 1).build()
        self.idx = 0

    def append(self, val: int) -> None:
        self.s.update(self.idx, self.idx, val, 0)
        self.idx += 1

    def addAll(self, inc: int) -> None:
        self.s.update(0, self.idx, inc, 0)

    def multAll(self, m: int) -> None:
        self.s.update(0, self.idx, m, 1)

    def getIndex(self, idx: int) -> int:
        return self.s.query(idx, idx)
