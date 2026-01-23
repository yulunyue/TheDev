from typing import List


class PnNode:
    left: "PnNode" = None
    right: "PnNode" = None
    is_remove = False

    def __init__(self, v):
        self.value = v

    def get_value(self):
        return self.value

    @classmethod
    def make(cls, array, func=None) -> List["PnNode"]:
        ret: List[PnNode] = []
        for i, v in enumerate(array):
            if func is not None:
                v = func(i, v)
            n = cls(v)
            if i != 0:
                n.set_left(ret[-1])
            ret.append(n)
        return ret

    def set_left(self, n):
        self.left = n
        if n:
            n.right = self

    def set_right(self, n: "PnNode"):
        self.right = n
        if n:
            n.left = self

    def remove(self):
        if self.left:
            self.left.set_right(self.right)
        elif self.right:
            self.right.set_left(self.left)
        self.is_remove = True
        return self

    def replace(self, node):
        if self.left:
            self.left.set_right(node)
        if self.right:
            self.right.set_left(node)
        self.is_remove = True

    def get_tail(self):
        ret = self
        while ret.left:
            ret = ret.left
        return ret

    def __lt__(self, p: "PnNode"):
        return self.get_value() < p.get_value()
