from common.util.export import logger, List

inf = float("inf")


class SegTreeNode:
    """
                              1[0-6]
                2[0-3]                      3[4-6]
         4[0-1]        5[2-3]         6[4-5]         7[6-6]
    8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    """

    todo: list
    value: list

    def __init__(self, n: int, *args) -> None:
        self.n = n
        self.size = 4 * n
        self.todo = [None] * self.size

        self.load(*args)

    def build(self, node, l, r):
        if l == r:
            self.do(node, l, r)
            return
        m = (l + r) // 2
        self.build(node * 2, l, m)  # 初始化左子树
        self.build(node * 2 + 1, m + 1, r)  # 初始化右子树
        self.up(node)

    def do(self, i, L, R, *v):
        raise NotImplementedError()

    def up(self, i):
        self.value[i] = self.merge(self.value[i * 2], self.value[i * 2 + 1])

    def merge(self, lv, rv):
        raise NotImplementedError()

    def query_array(self, i, l, r, L, R):
        if l <= L and R <= r:
            return self.value[i]
        self.down(i, L, R)
        m = (L + R) // 2
        if r <= m:
            return self.query_array(i * 2, l, r, L, m)
        if m < l:
            return self.query_array(i * 2 + 1, l, r, m + 1, R)
        lv = self.query_array(i * 2, l, r, L, m)
        rv = self.query_array(i * 2 + 1, l, r, m + 1, R)
        return self.merge(lv, rv)

    def query(self, l, r):
        return self.query_array(1, l, r, 0, self.n)

    def query_first(self, k):
        pass

    def load(self, *args):
        raise NotImplementedError()

    def update_area(self, i, l, r, L, R, *v):
        if l <= L and R <= r:
            self.do(i, L, R, *v)
            return
        self.down(i, L, R)
        m = (L + R) // 2
        if m < r:
            self.update_area(i * 2 + 1, l, r, m + 1, R, *v)
        if m >= l:
            self.update_area(i * 2, l, r, L, m, *v)
        self.up(i)

    def update(self, l, r, *v):
        self.update_area(1, l, r, 0, self.n, *v)

    def down(self, i, L, R):
        if self.todo[i] is not None:
            m = (L + R) // 2
            self.do(i * 2, L, m, *self.todo[i])
            self.do(i * 2 + 1, m + 1, R, *self.todo[i])
            self.todo[i] = None

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

    def to_str(self):
        ret = []

        def util(i, depth, l, r):
            info = f"{' '*depth}{l}-{r}: "
            if self.value[i] is not None:
                info += f"{self.value[i]} "
            if self.todo[i] is not None:
                info += f"todo={self.todo[i]}"
            ret.append(info)
            if l == r:
                return
            m = (l + r) // 2
            util(i * 2, depth + 2, l, m)
            util(i * 2 + 1, depth + 2, m + 1, r)

        util(1, 0, 0, self.n)
        return "\n".join(["-" * 10] + ret + ["-" * 10])
