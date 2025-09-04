from app.yly.envs.cg.cw.model.constant import C
from common.util.export import logger, List, defaultdict, Dict
from .b_line_help import BM
from .path import Path


class ShapeBase:
    x: int = -1
    owner = C.OWNER_NEUTRAL
    unit_type = C.TYPE_NULL

    def __init__(self, g, shape_type, y, x):
        from app.yly.envs.cg.cw.shape.world import World

        self.y: int = y
        self.x: int = x
        self.shape_type = shape_type
        self.g: World = g

    def load(self, unit_id, unit_type, hp, owner):
        self.unit_type = unit_type
        self.owner = owner
        self.hp = hp
        self.unit_id = unit_id
        return self

    def reset(self):
        self.unit_type = C.TYPE_NULL
        self.owner = C.OWNER_NEUTRAL
        self.unit_id = None
        return self

    def view(self):
        def f(s):
            return f"{s}{self.unit_id%10}"

        if self.shape_type == C.TYPE_OBS:
            return "##"
        if self.unit_type == C.TYPE_CULT_LEADER:
            return f("A" if self.owner == 0 else "B")
        if self.unit_type == C.TYPE_CULTIST:
            o = "DEC"[self.owner]
            return f(o)
        return "  "

    @property
    def k(self):
        return self.y, self.x

    nexts_tiles: List["ShapeBase"] = None

    def get_nexts_tiles(self) -> List["ShapeBase"]:
        if self.nexts_tiles is not None:
            return self.nexts_tiles
        self.nexts_tiles: List[ShapeBase] = []
        for dy, dx in C.DR:
            y, x = self.y + dy, self.x + dx
            if y < 0 or x < 0 or y >= self.g.height or x >= self.g.width:
                continue
            p = self.g.grid[y][x]
            if p.shape_type == C.TYPE_OBS:
                continue
            self.nexts_tiles.append(p)
        return self.nexts_tiles

    def get_dis(self, aim: "ShapeBase", default_value=None):
        return self.path.shpae_dis.get(aim.k, default_value)

    def get_abs_dis(self, aim: "ShapeBase"):
        return abs(self.x - aim.x) + abs(self.y - aim.y)

    _path: Path = None

    @property
    def path(self):
        if self._path:
            return self._path
        q: List[ShapeBase] = [self]
        l = 1

        self._path = Path(self)
        self._path.shpae_dis[self.k] = 0
        while q:
            tmp = q
            q = []
            for s in tmp:
                for p in s.get_nexts_tiles():
                    if p.k in self._path.shpae_dis:
                        continue
                    self._path.shpae_dis[p.k] = l
                    if p.unit_type == C.TYPE_NULL:
                        q.append(p)
                    else:
                        self._path.add_shape(l, p)
            l += 1
        return self._path

    def calc_dis(self, ss: List["ShapeBase"]):
        min_v, sum_v, max_v = float("inf"), 0, float("-inf")
        for d in ss:
            v = self.get_dis(d, -1)
            if v == -1:
                continue
            if v < min_v:
                min_v = v
            if v > max_v:
                max_v = v
            sum_v += v
        return min_v, sum_v, max_v
