from app.yly.game.envs.cf4.shape.point import Point
from app.yly.game.envs.cf4.model.constant import C
from common.util.export import List, Dict


class Column:
    def __init__(self, p, idx, height):
        from app.yly.game.envs.cf4.shape.grid import Grid

        self.p: Grid = p
        self.idx = idx
        self.height = height
        self.mask = (1 << height) - 1
        self.mask_pos = [(1 << i) - 1 for i in range(height)]
        self.state = 1
        self.pts: List[Point] = [Point(p, i, idx) for i in range(height)]
        self.top = 0

    def set_state(self, state: int):
        if self.state == state:
            return
        self.state = state
        self.top = state.bit_length() - 1
        for i in range(self.height):
            if i < self.top:
                self.pts[i].set_value(state & 1)
            else:
                self.pts[i].set_value(2)
            state = state >> 1
        return self

    def put(self, player_id):
        return C.mask_encode(
            self.p.board,
            self.p.shape,
            self.idx * self.height + self.top,
            player_id,
        )
