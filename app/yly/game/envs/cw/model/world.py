from app.yly.game.envs.cw.model.shape import ShapeBase
from app.yly.game.envs.cw.model.constant import C
from app.yly.game.envs.cw.model.action import Action
from common.util.export import List, Dict, logger
import random
from .path import Path


class World:
    maps = None

    def load(self, width=13, height=7, maps=None, shapes=None, **kw):
        self.width = width
        self.height = height
        self.maps = maps
        self.grid: List[List[ShapeBase]] = []
        self.shapes: List[ShapeBase] = [ShapeBase(self) for _ in range(C.UNITS_NUM)]
        self.cultists: List[Dict[int, ShapeBase]] = [dict(), dict(), dict()]
        self.cult_leaders: List[ShapeBase] = [None, None]
        for i in range(height):
            tmp = []
            for j in range(width):
                s = ShapeBase(self).load(i, j, maps[i][j])
                tmp.append(s)
            self.grid.append(tmp)
        self.set_shapes(shapes)

        return self

    def set_player_id(self, player_id):
        self.player_id: int = player_id
        return self

    def set_shapes(self, shapes: List[List[int]]):
        if shapes is None:
            return
        self.units = shapes
        self.path_info: Dict[str, Path] = dict()
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
            if unit_type == C.TYPE_CULT_LEADER:
                self.cult_leaders[owner] = s
            s.set_info(owner, hp, unit_id)
        for g in self.cultists[self.player_id].values():
            for s in g.get_nexts_tiles():
                if s.k in self.path_info:
                    continue
                self.path_info[s.k] = s.bfs_find_action(g.owner)

    def get_action(self):
        max_score = None
        best_action: Action = None
        for src in self.cultists[self.player_id].values():
            srcs = src.get_nexts_tiles()
            for dst in srcs:
                if src.owner == dst.owner:
                    continue
                action = Action(self, src, dst)
                score = action.calc()
                if score is None:
                    continue
                if max_score is None or score > max_score:
                    max_score = score
                    best_action = action
        return best_action.get_action() if best_action is not None else C.ACTION_WAIT

    def to_json(self):
        return dict(
            width=self.width, height=self.height, maps=self.maps, shapes=self.units
        )

    def __repr__(self):

        s = [
            f"hp0:{self.cult_leaders[0].hp} hp1: {self.cult_leaders[1].hp}",
            ["#"] * (self.width + 2),
        ]
        for i, row in enumerate(self.grid):
            tmp = ["#"]
            for j, c in enumerate(row):
                tmp.append(c.view())
            tmp.append("#")
            s.append(tmp)
        s.append(["#"] * (self.width + 2))
        return "\n".join(["".join(r) for r in s])
