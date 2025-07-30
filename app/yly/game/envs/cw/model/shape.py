from app.yly.game.envs.cw.model.constant import C
from common.util.export import logger, List, defaultdict, Dict


class ShapeBase:
    x: int = -1
    unit_type = None
    unit_id = None
    owner = C.OWNER_NEUTRAL

    def __init__(self, g, shape_type):
        from app.yly.game.envs.cw.model.world import World

        self.unit_type = self.shape_type = shape_type
        self.g: World = g

    def load(self, unit_id, unit_type, hp, x, y, owner):
        self.y: int = y
        self.x: int = x
        self.unit_type = unit_type
        self.owner = owner
        self.hp = hp
        self.unit_id = unit_id
        return self

    def reset(self):
        self.unit_type = self.shape_type
        self.owner = 2
        self.unit_id = None
        return self

    def view(self):
        def f(s):
            return f"{s}{self.unit_id%10}"

        if self.unit_type == C.TYPE_OBS:
            return "##"
        if self.unit_type == C.TYPE_NULL:
            return f"  "
        if self.unit_type == C.TYPE_CULT_LEADER:
            return f("A" if self.owner == 0 else "B")
        if self.unit_type == C.TYPE_CULTIST:
            o = "DEC"[self.owner]
            return f(o)
        # print(self.shape_type)
        return f(self.unit_type)

    def __repr__(self):
        return f"id:{self.unit_id}, type:{self.view()}, hp:{self.hp}, owner:{self.owner}, y:{self.y}, x:{self.x}"

    @property
    def k(self):
        return self.y, self.x

    def get_nexts_tiles(self):
        ret: List[ShapeBase] = []
        for dy, dx in C.DR:
            y, x = self.y + dy, self.x + dx
            if y < 0 or x < 0 or y >= self.g.height or x >= self.g.width:
                continue
            p = self.g.grid[y][x]
            if p.unit_type == C.TYPE_OBS:
                continue
            ret.append(p)
        return ret

    def get_dis(self, aim: "ShapeBase"):
        if self.unit_type != C.TYPE_NULL:
            raise Exception(self)
        return self.g.path_info[self.k].shpae_dis[aim.k]

    def bfs_find_action(self, player_id):
        q: List[ShapeBase] = [self]
        vt = dict()
        l = 1
        from .path import Path

        path = Path()
        while q:
            tmp = q
            q = []
            for s in tmp:
                for p in s.get_nexts_tiles():
                    if p.k in vt:
                        continue
                    vt[p.k] = l
                    if p.unit_type == C.TYPE_NULL:
                        q.append(p)
                    else:
                        if p.unit_type == self.unit_type:
                            continue
                        if p.owner == player_id:
                            continue
                        path.add_shape(l, p)
            l += 1
        return path
