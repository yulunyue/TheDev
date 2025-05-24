from app.yly.algo.cg.cw.constant import C


class ShapeBase:
    type = None
    owner = None
    hp = None
    unit_id = None

    def load(self, y, x):
        self.y, self.x = y, x
        return self

    def to_json(self):
        return dict(
            y=self.y,
            x=self.x,
            type=self.type,
            owner=self.owner,
            hp=self.hp,
            unit_id=self.unit_id,
        )
