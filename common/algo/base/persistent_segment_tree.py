from common.util.export import List
from .segtree import SegTreeNode


class D3SegmentTree(SegTreeNode):
    cnt = 0
    _left: "D3SegmentTree"
    _right: "D3SegmentTree"

    def clone(self):
        return self.__class__().set_range(self.l, self.r)

    def add(self, idx, v):
        o: D3SegmentTree = self.clone()
        o.cnt, o._left, o._right = self.cnt, self._left, self._right
        if self.l == idx == self.r:
            o.do(v)
            return o
        if idx <= self.m:
            o._left = self._left.add(idx, v)
        else:
            o._right = self._right.add(idx, v)
        o.up()
        return o

    def kth(self, l: "D3SegmentTree", k: int):
        if self.l == self.r:
            return self.l
        lcnt = self.left.cnt - l.left.cnt
        if k <= lcnt:
            return self.left.kth(l.left, k)
        return self.right.kth(l.right, k - lcnt)
