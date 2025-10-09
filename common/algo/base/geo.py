from typing import List


class Vec:
    __slots__ = "x", "y"

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __sub__(self, b: "Vec") -> "Vec":
        return Vec(self.x - b.x, self.y - b.y)

    def det(self, b: "Vec") -> int:
        return self.x * b.y - self.y * b.x

    def dot(self, b: "Vec") -> int:
        return self.x * b.x + self.y * b.y


class Geo:

    def set_points(self, vecs):
        self.vecs: List[Vec] = vecs
        return self

    # Andrew 算法，计算 points 的上凸包
    def andrew_convex_hull(self):
        q: List[Vec] = []
        for p in self.vecs:
            while len(q) > 1 and (q[-1] - q[-2]).det(p - q[-1]) >= 0:
                q.pop()
            q.append(p)
        return q
