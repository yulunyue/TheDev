from typing import NoReturn
from common.util.export import logger

inf = float("inf")


class SegTreeNode:
    """
                              1[0-6]
                2[0-3]                      3[4-6]
         4[0-1]        5[2-3]         6[4-5]         7[6-6]
    8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    """

    __slots__ = "_left", "_right"

    def __init__(self, idx=1) -> None:
        self.idx = idx
        self.todo = 0
        self._left: SegTreeNode = None
        self._right: SegTreeNode = None

    def do(self, v):
        self.value = v

    def up(self):
        self.value = self.merge(self.left.value, self.right.value)

    def merge(self, lv, rv):
        return lv + rv

    def set_range(self, l, r):
        self.l = l
        self.r = r
        self.size = r - l + 1
        self.m = (l + r) // 2
        return self

    @property
    def left(self):
        if not self._left:
            self._left = self.__class__(self.idx * 2).set_range(self.l, self.m)
        return self._left

    @property
    def right(self):
        if not self._right:
            self._right = self.__class__(
                self.idx * 2 + 1,
            ).set_range(self.m + 1, self.r)
        return self._right

    def query(self, l, r):
        if l <= self.l and self.r <= r:
            return self.value
        self.down()
        if r <= self.m:
            return self.left.query(l, r)
        if self.m < l:
            return self.right.query(l, r)
        lv = self.left.query(l, r)
        rv = self.right.query(l, r)
        return self.merge(lv, rv)

    def init(self, nums):
        pass

    def build(self, *args):
        if self.l == self.r:
            self.init(*args)
            return self
        self.left.build(*args)
        self.right.build(*args)
        self.up()
        return self

    def update(self, l, r, value):
        if l <= self.l and self.r <= r:
            self.do(value)
            return
        self.down()
        if self.m < r:
            self.right.update(l, r, value)
        if self.m >= l:
            self.left.update(l, r, value)
        self.up()

    def down(self):
        if self.todo:
            self.left.do(self.todo)
            self.right.do(self.todo)
            self.todo = 0

    def find(self, ql: int, qr: int, target: int) -> int:
        if self.l > qr or self.r < ql:
            return -1
        if self.l == self.r:
            return self.l
        self.down()
        idx = self.left.find(ql, qr, target)
        if idx < 0:
            # 去右子树找
            idx = self.right.find(ql, qr, target)
        return idx

    def show(self):
        return f"v:{self.value}"

    def __str__(self):
        ret = []

        def util(p: SegTreeNode, depth):
            ret.append(f"{' '*depth}{p.l}-{p.r}: v={p.show()} todo={p.todo}")
            if p.l == p.r:
                return
            util(p.left, depth + 2)
            util(p.right, depth + 2)

        util(self, 0)
        return "\n".join(["-" * 10] + ret + ["-" * 10])
