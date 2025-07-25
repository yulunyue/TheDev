from app.yly.game.envs.cw.model.shape import ShapeBase
from app.yly.game.envs.cw.model.constant import C
from common.util.export import List


class World:
    def load(self, width=13, height=7, maps=None):
        self.width = width
        self.height = height
        self.maps = maps
        self.grid: List[List[ShapeBase]] = []
        for i in range(height):
            tmp = []
            for j in range(width):
                s = ShapeBase().load(i, j, maps[i][j])
                tmp.append(s)
            self.grid.append(tmp)
        return self

    def set_shape(self, i: int, j: int, type: str, owner=None, hp=None, unit_id=None):
        g = self.grid[i][j]
        g.type = type
        self.grid[i][j].owner = owner
        self.grid[i][j].hp = hp
        self.grid[i][j].unit_id = unit_id

    def get_action(self):
        return "WAIT"

    def to_json(self):
        return dict(width=self.width, height=self.height)
