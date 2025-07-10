from app.yly.game.envs.cf4.shape.point import Point
from common.util.export import List, Dict


class Line:
    LINE_MAP: Dict[str, "Line"] = dict()

    def __init__(self, drx):
        self.drx = drx
        self.pts: List[Point] = [None] * 4
        self.value_ct = [0, 0, 4]

    @staticmethod
    def new_line(y, x, drx):
        k = y, x, drx
        if k not in Line.LINE_MAP:
            Line.LINE_MAP[k] = Line(drx)
        return Line.LINE_MAP[k]

    def set_point(self, idx, pt: Point):
        self.pts[idx] = pt
        pt.lines[self.drx, idx] = self
        return self

    def change_value(self, pt: Point, pos_idx, last_value, value):
        self.value_ct[value] += 1
        self.value_ct[last_value] -= 1
        player_id, change_value = value, -1
        if value == 2:
            player_id, change_value = last_value, 1

        if self.value_ct[1 - player_id] == 0 and self.value_ct[player_id]:
            pt.g.line_state_change(
                self,
                pos_idx,
                player_id,
                self.value_ct[player_id] + change_value,
                self.value_ct[player_id],
            )

    def __str__(self):
        r = []
        s = ""
        for v in self.pts:
            r.append(f"{v.x}{v.y}")
            if v.value == 2:
                s += "*"
            else:
                s += str(v.value)
        r = "->".join(r)
        return f"dr:{self.drx}; pt:{r}; s:{s}"
