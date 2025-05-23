from app.yly.algo.cg.cw.constant import C


class ShapeBase:
    type = None
    owner = None
    hp = None
    unit_id = None

    def load(self, y, x):
        self.y, self.x = y, x
        return self
