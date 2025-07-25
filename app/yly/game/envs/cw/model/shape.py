from app.yly.game.envs.cw.model.constant import C


class ShapeBase:

    owner = None
    hp = None
    unit_id = None

    def load(self, y, x, shape_type):
        self.y, self.x = y, x
        self.shape_type = shape_type
        return self

    def to_json(self):
        return dict(
            y=self.y,
            x=self.x,
            shape_type=self.shape_type,
            owner=self.owner,
            hp=self.hp,
            unit_id=self.unit_id,
        )
