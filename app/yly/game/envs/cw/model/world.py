from app.yly.game.envs.cw.model.shape import ShapeBase
from app.yly.game.envs.cw.model.constant import C
from common.util.export import List


class World:
    maps = None

    def load(self, width=13, height=7, maps=None, shapes=None, **kw):
        self.width = width
        self.height = height
        self.maps = maps
        self.grid: List[List[ShapeBase]] = []
        self.set_shapes(shapes)
        for i in range(height):
            tmp = []
            for j in range(width):
                s = ShapeBase().load(i, j, maps[i][j])
                tmp.append(s)
            self.grid.append(tmp)
        return self

    def set_shapes(self, shapes):
        if shapes is None:
            return
        self.units = shapes
        self.shapes: List[ShapeBase] = []
        for unit_id, unit_type, hp, x, y, owner in shapes:
            self.shapes.append(
                ShapeBase().load(y, x, unit_type).set_info(owner, hp, unit_id)
            )

    def get_action(self):
        return "WAIT"

    def to_json(self):
        return dict(
            width=self.width, height=self.height, maps=self.maps, shapes=self.units
        )

    def __repr__(self):
        s = [["##"] * (self.width + 1)]
        for i, row in enumerate(self.grid):
            tmp = ["#"]
            for j, c in enumerate(row):
                tmp.append(str(c))
            tmp.append("#")
            s.append(tmp)
        for n in self.shapes:
            s[n.y + 1][n.x + 1] = str(n)
        s.append(["##"] * (self.width + 1))
        return "\n".join(["".join(r) for r in s])
