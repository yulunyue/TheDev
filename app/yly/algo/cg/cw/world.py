from app.yly.algo.cg.cw.shape import ShapeBase
from app.yly.algo.cg.cw.constant import C


class World:
    def __init__(self, width=13, height=7):
        self.width = width
        self.height = height
        self.grid = [
            [ShapeBase().load(i, j) for j in range(width)] for i in range(height)
        ]

    def set_shape(self, i: int, j: int, type: str, owner=None, hp=None, unit_id=None):
        self.grid[i][j].type = type
        self.grid[i][j].owner = owner
        self.grid[i][j].hp = hp
        self.grid[i][j].unit_id = unit_id

    def get_action(self):
        return "WAIT"

    def to_json(self):
        ret = []
        for row in self.grid:
            for col in row:
                ret.append(col.to_json())
        return ret
