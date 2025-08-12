from .constant import C


class Player:

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

    def set_grid(self, g):
        from .grid import Grid

        self.g: Grid = g
        return self

    def view(self):

        if self.entity_type == C.EXPLORER:
            return f"e{self.key}"
        return f"p{self.key}"

    @property
    def cell(self):
        return self.g.borads[self.y][self.x]
