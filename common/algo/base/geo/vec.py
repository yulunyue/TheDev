class Vec:
    __slots__ = "x", "y"

    def __init__(self, x: int, y: int = None):
        if y is None:
            self.x, self.y = x[0], x[1]
        else:
            self.x, self.y = x, y

    def __sub__(self, b: "Vec") -> "Vec":
        return Vec(self.x - b.x, self.y - b.y)

    def det(self, b: "Vec") -> int:  # 四边形的面积,正负表示逆顺方向
        return self.x * b.y - self.y * b.x

    def dot(self, b: "Vec") -> int:  # a*b*cos
        return self.x * b.x + self.y * b.y

    def is_left(self, b: "Vec"):  # 平行同方向也算
        return self.det(b) >= 0

    def is_right(self, b: "Vec"):  # 平行逆方向也算
        return self.det(b) <= 0

    def area(self, b: "Vec"):
        return abs(self.det(b))
