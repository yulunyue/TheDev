from typing import List


class BlineHelp:
    def __init__(self):
        self.maps = dict()

    def bresenham_line(self, y1, x1, chen):
        """
        使用 Bresenham 算法在网格上绘制从 (x0, y0) 到 (x1, y1) 的直线。
        返回直线路径上的所有像素坐标列表。尽可能的直线
        """
        points = []
        x0 = y0 = 0
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1  # x 方向步进（支持反向绘制）
        sy = 1 if y0 < y1 else -1  # y 方向步进（支持反向绘制）
        err = dx - dy  # 初始误差项

        while x0 != x1 or y0 != y1:

            e2 = 2 * err
            if e2 > -dy:  # 误差项决定 x 步进
                err -= dy
                x0 += sx
            if e2 < dx:  # 误差项决定 y 步进
                err += dx
                y0 += sy
            points.append((y0 * chen, x0 * chen))
        return points[:-1]

    def get(self, y, x) -> List[List[int]]:
        k = y, x
        c = 1
        if y < 0:
            y, x, c = -y, -x, -1
        if k in self.maps:
            return self.maps[k]
        self.maps[k] = self.bresenham_line(y, x, c)
        return self.maps[k]

    def draw(self, y0, x0, y1, x1):
        ret = [["*"] * 10 for _ in range(5)]
        ret[y0][x0] = "A"
        for y, x in self.get(y1 - y0, x1 - x0):
            ret[y0 + y][x0 + x] = "B"
        return "\n" + "\n".join(["".join(v) for v in ret])


BM = BlineHelp()
