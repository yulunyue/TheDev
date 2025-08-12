from .constant import C
from common.util.export import List, Dict, logger


class Shape:

    def __init__(self, y, x, entity_type):
        self.x = x
        self.y = y
        self.entity_type = entity_type
        self.nexts: List[Shape] = None

    def get_nexts(self):
        if self.entity_type == C.TYPE_WALL:
            return []
        if self.nexts is not None:
            return self.nexts
        self.nexts = []
        for dy, dx in C.DR:
            y, x = self.y + dy, self.x + dx
            if y < 0 or x < 0 or y >= self.g.height or x >= self.g.width:
                continue
            if self.entity_type == C.TYPE_WALL:
                continue
            self.nexts.append(self.g.borads[y][x])
        return self.nexts

    def set_grid(self, g):
        from .grid import Grid

        self.g: Grid = g
        self.init()
        return self

    def view(self):
        if self.entity_type == C.TYPE_NULL:
            return "  "
        if self.entity_type == C.TYPE_WALL:
            return "##"
        return f"{self.entity_type}{self.entity_type}"

    @property
    def pos(self):
        return self.y, self.x

    def init(self):

        self.steps: List[List[Shape]] = []
        self.dis: Dict[str, Shape] = {self.pos: 0}
        q = [self]
        while q:
            self.steps.append(q)
            q = []
            for u in self.steps[-1]:
                for v in u.get_nexts():
                    if u.pos in self.dis:
                        continue
                    self.dis[u.pos] = len(self.steps)
                    q.append(v)
