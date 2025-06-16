from typing import NoReturn


inf = float("inf")


class SegTreeNode:
    """
                              1[0-6]
                2[0-3]                      3[4-6]
         4[0-1]        5[2-3]         6[4-5]         7[6-6]
    8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    """

    def __init__(self, idx=1) -> None:
        self.idx = idx
        self.todo = 0
        self.value = None
        self._left: SegTreeNode = None
        self._right: SegTreeNode = None

    def do(self, v):
        pass

    def up(self):
        pass

    def merge(self, l, r):
        pass

    def set_range(self, l, r):
        self.l = l
        self.r = r
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

    def build(self):
        if self.l == self.r:
            self.do()
            return
        self.left.build()
        self.right.build()
        self.up()

    def update(self, l, r, value):
        if l <= self.l and self.r <= r:
            self.do(value)
            return
        self.down()
        if self.m >= l:
            self.left.update(l, r, value)
        if self.m < r:
            self.right.update(l, r, value)
        self.up()

    def down(self):
        if self.todo:
            self.left.do(self.todo)
            self.right.do(self.todo)
            self.todo = 0

    def __str__(self):
        ret = []

        def util(p: SegTreeNode, depth):
            ret.append(f"{' '*depth}{p.l}-{p.r}:{p.value}")
            if p.l == p.r:
                return
            util(p.left, depth + 2)
            util(p.right, depth + 2)

        util(self, 0)
        return "\n".join(ret)
