from app.yly.game.envs.cw.model.shape import ShapeBase
from app.yly.game.envs.cw.model.constant import C
from app.yly.game.envs.cw.model.action import Action
from common.util.export import List, Dict, logger
import random


class World:
    maps = None

    def load(self, width=13, height=7, maps=None, shapes=None, **kw):
        self.width = width
        self.height = height
        self.maps = maps
        self.grid: List[List[ShapeBase]] = []
        self.shapes: List[ShapeBase] = [ShapeBase(self) for _ in range(C.UNITS_NUM)]
        self.cultists: List[Dict[int, ShapeBase]] = [dict(), dict(), dict()]
        for i in range(height):
            tmp = []
            for j in range(width):
                s = ShapeBase(self).load(i, j, maps[i][j])
                tmp.append(s)
            self.grid.append(tmp)
        self.set_shapes(shapes)
        self.path_info = dict()
        return self

    def set_player_id(self, player_id):
        self.player_id: int = player_id
        return self

    def set_shapes(self, shapes: List[List[int]]):
        if shapes is None:
            return
        self.units = shapes
        for unit_id, unit_type, hp, x, y, owner in shapes:
            s = self.shapes[unit_id]
            if s.x == -1:
                s.load(y, x, unit_type)
                self.grid[y][x] = s
                self.cultists[owner][unit_id] = s
            else:
                if s.x != x or s.y != y:
                    self.grid[s.y][s.x] = self.grid[y][x]
                    self.grid[y][x].load(s.y, s.x, C.TYPE_NULL)
                    self.grid[y][x] = s
                    s.load(y, x, unit_type)
                if s.owner != owner:
                    self.cultists[owner][unit_id] = self.cultists[s.owner].pop(unit_id)
            s.set_info(owner, hp, unit_id)
        self.path_info.clear()
        for s in self.shapes:
            if s.owner == self.player_id:
                s.bfs_find_action()

    def get_action(self):
        max_score = float("-inf")
        best_action: Action = None
        for src in self.cultists[self.player_id].values():
            srcs = src.get_nexts_tiles()
            if src.unit_type == C.TYPE_CULTIST:
                srcs.append(self.cult_leaders[1 - self.player_id])
            for dst in srcs:
                if src.owner == dst.owner:
                    continue
                a = Action(src, dst).calc()
                if a.score > max_score:
                    max_score = a.score
                    best_action = a
        return best_action.get_action() if best_action is not None else C.ACTION_WAIT

    def get_best_action(self):
        p = self.cult_leaders[self.player_id]
        mn = float("inf")
        dst: ShapeBase = None
        for n in p.get_nexts_tiles():
            if n.shape_type == C.TYPE_CULTIST and n.owner != self.player_id:
                return f"{p.unit_id} CONVERT {n.unit_id}"
            nodes, dis = n.bfs_find_action()
            if not dis:
                continue
            if dis[0] < mn:
                mn = dis[0]
                dst = n
        if dst is None:
            p, dst = self.cultists_get_best()
        if dst is not None:
            return f"{p.unit_id} MOVE {dst.x} {dst.y}"
        # logger.map(nodes=nodes, dis=dis)
        return "WAIT"

    def to_json(self):
        return dict(
            width=self.width, height=self.height, maps=self.maps, shapes=self.units
        )

    def __repr__(self):
        s = [["#"] * (self.width + 2)]
        for i, row in enumerate(self.grid):
            tmp = ["#"]
            for j, c in enumerate(row):
                tmp.append(c.view())
            tmp.append("#")
            s.append(tmp)
        s.append(["#"] * (self.width + 2))
        return "\n".join(["".join(r) for r in s])
