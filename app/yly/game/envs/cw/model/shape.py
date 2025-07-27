from app.yly.game.envs.cw.model.constant import C
from common.util.export import logger, List, defaultdict, Dict


class ShapeBase:
    x: int = -1
    unit_type = None
    unit_id = None
    owner = C.OWNER_NEUTRAL

    def __init__(self, g):
        from app.yly.game.envs.cw.model.world import World

        self.g: World = g

    def load(self, y, x, shape_type):
        self.y: int = y
        self.x: int = x
        self.shape_type = shape_type
        return self

    def set_info(self, owner, hp, unit_id):
        self.owner = owner
        self.hp = hp
        self.unit_id = unit_id
        return self

    def view(self):
        if self.shape_type == C.TYPE_OBS:
            return "#"
        if self.shape_type == C.TYPE_NULL:
            return f" "
        if self.shape_type == 1:
            return "A" if self.owner == 0 else "B"
        if self.shape_type == C.TYPE_CULTIST:
            o = "DEC"[self.owner]
            return f"{o}"
        # print(self.shape_type)
        return f"{self.shape_type}"

    def __repr__(self):
        return f"id:{self.unit_id}, type:{self.shape_type}, hp:{self.hp}, owner:{self.owner}, y:{self.y}, x:{self.x}"

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
            if p.shape_type == C.TYPE_OBS:
                continue
            ret.append(p)
        return ret

    def bfs_find_action(self):
        q: List[ShapeBase] = [self]
        vt = dict()
        l = 0
        while q:
            tmp = q
            q = []
            for s in tmp:
                for p in s.get_nexts_tiles():
                    if p.shape_type == C.TYPE_NULL:
                        if p.k not in vt:
                            vt[p.k] = l
                            q.append(p)
                    else:
                        if p.shape_type == self.shape_type:
                            continue
                        if p.owner == self.owner:
                            continue
                        self.g.path_info[self.k, p.k] = l
            l += 1
