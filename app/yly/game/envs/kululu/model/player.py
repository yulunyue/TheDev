from app.yly.game.envs.kululu.model.constant import C


class Shape:

    def __init__(self, x, y, entity_type, key):
        self.x = x
        self.y = y
        self.entity_type = entity_type
        self.key = key

    def view(self):
        if self.entity_type == C.EXPLORER:
            return f"E{self.key}"
        if self.entity_type == C.WANDERER:
            return f"S{str(self.key)[-1]}"
        if self.entity_type == ".":
            return "  "
        if self.entity_type == "#":
            return "##"
        return f"{self.entity_type}{str(self.key)[-1]}"

    @property
    def pos(self):
        return self.y, self.x


class Player(Shape):

    def __init__(self, entity_type, key, x, y, param_0, param_1, param_2) -> None:
        self.x = int(x)
        self.y = int(y)
        self.entity_type = entity_type
        self.key = key
        self.param_0 = param_0
        self.param_1 = param_1
        self.param_2 = param_2

    def dump(self):
        return [
            self.entity_type,
            self.key,
            self.x,
            self.y,
            self.param_0,
            self.param_1,
            self.param_2,
        ]
