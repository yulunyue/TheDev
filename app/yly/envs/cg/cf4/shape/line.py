from ..shape.point import Point, C
from common.util.export import List, Dict


class Line:
    LINE_MAP: Dict[str, "Line"] = dict()

    def __init__(self, k):
        self.k = k
        self.drx = k[2]
        self.pts: List[Point] = [None] * 4
        self.value_ct = [0, 0]

    @staticmethod
    def new_line(y, x, drx):
        k = y, x, drx
        if k not in Line.LINE_MAP:
            Line.LINE_MAP[k] = Line(k)
        return Line.LINE_MAP[k]

    def set_point(self, idx, pt: Point):
        self.pts[idx] = pt
        pt.lines[self.drx, idx] = self
        return self

    def change_value(self, pt: Point, pos_idx, player_id, num):
        l0, l1 = self.value_ct
        self.value_ct[player_id] += num
        pt.g.line_state_change(
            self, pos_idx, player_id, l0, l1, self.value_ct[0], self.value_ct[1]
        )

    def __str__(self):
        return f"y:{self.k[0]}; x:{self.k[1]}; dr:{C.DR[self.drx]}"
