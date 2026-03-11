from common.util.export import List, deque
from .vec import Vec


class Andrew:
    def __init__(self):
        self.q: deque[Vec] = deque()

    def append_down_det(self, x, y=None):
        p = Vec(x, y)
        while len(self.q) > 1:
            a1 = self.q[-1] - self.q[-2]
            a2 = p - self.q[-1]
            if not a1.on_the_right_of(a2):
                break
            self.q.pop()
        self.q.append(p)
        return self

    def run(self, pts):
        """
        pts 已经排序好
        """
        self.q: deque[Vec] = deque()
        for v in pts:
            self.append_down_det(v)
        q, self.q = self.q, deque()
        for v in reversed(pts):
            self.append_down_det(v)
        return q[:-1] + self.q[:-1]
