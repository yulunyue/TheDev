from typing import List


class PnNode:
    left: "PnNode" = None
    right: "PnNode" = None

    def __init__(self, v):
        self.value = v

    @classmethod
    def make(cls, array) -> List["PnNode"]:
        ret: List[PnNode] = []
        for i, v in enumerate(array):
            n = PnNode(v)
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
        return self
