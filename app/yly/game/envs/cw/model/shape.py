from app.yly.game.envs.cw.model.constant import C


class ShapeBase:

    def load(self, y, x, shape_type):
        self.y, self.x = y, x
        self.shape_type = shape_type
        return self

    def set_info(self, owner, hp, unit_id):
        self.owner = owner
        self.hp = hp
        self.unit_id = unit_id
        return self

    def __repr__(self):
        if self.shape_type == "x":
            return "##"
        if self.shape_type == ".":
            return f"  "
        if self.shape_type == 1:
            return "AA" if self.owner == 0 else "BB"
        if self.shape_type == 0:
            o = "ABC"[self.owner]
            return f"{o}C"
        # print(self.shape_type)
        return f"{self.shape_type}{self.owner}"
