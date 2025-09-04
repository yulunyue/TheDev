from common.util.export import List, Dict, Tuple
from ..model.constant import C
from .b_line_help import BM


class Path:
    def __init__(self, root):
        from .cell import ShapeBase

        self.root: ShapeBase = root
        # self.shapes: List[List[ShapeBase]] = [[], [], []]
        self.shpae_dis: Dict[str, int] = {}
        self.can_shoot_units: List[Tuple[int, ShapeBase]] = []
        # self.leaders: List[ShapeBase] = [None, None]

    def can_shoot(self, y, x):
        for dy, dx in BM.get(y - self.root.y, x - self.root.x):
            y, x = self.root.y + dy, self.root.x + dx
            if self.root.g.grid[y][x].unit_type != C.TYPE_NULL:
                return False
        return True

    def add_shape(self, dis, aim):
        from .cell import ShapeBase

        s: ShapeBase = aim
        if s.unit_type != C.TYPE_NULL and s.owner == 1 - self.root.owner:
            if dis < C.VALUE_DAMAGE_MAX:
                if self.can_shoot(s.y, s.x):
                    self.can_shoot_units.append([s, C.VALUE_DAMAGE_MAX - dis])
        self.shpae_dis[s.k] = dis
