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
        self.null_shapes: List[ShapeBase] = []
        for i in range(height):
            tmp = []
            for j in range(width):
                s = ShapeBase(self, maps[i][j]).load(None, maps[i][j], None, i, j, None)
                if s.shape_type == C.TYPE_NULL:
                    self.null_shapes.append(s)
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
        self.cultists: List[Dict[int, ShapeBase]] = [dict(), dict(), dict()]
        self.cult_leaders: List[ShapeBase] = [None, None]
        self.hp = [0, 0, 0]
        self.units = shapes
        self.path_info: Dict[str, Path] = dict()
        for s in self.null_shapes:
            s.reset()
        for unit_id, unit_type, hp, x, y, owner in shapes:
            s = self.grid[y][x]
            s.load(unit_id, unit_type, hp, x, y, owner)
            self.cultists[owner][unit_id] = s
            self.hp[owner] += hp
            if unit_type == C.TYPE_CULT_LEADER:
                self.cult_leaders[owner] = s
        for g in self.cultists[self.player_id].values():
            for s in g.get_nexts_tiles():
                if s.k in self.path_info:
                    continue
                self.path_info[s.k] = s.bfs_find_action(g.owner)

    def get_action(self):
        max_score = None
        best_action = C.ACTION_WAIT
        for src in self.cultists[self.player_id].values():
            srcs = src.get_nexts_tiles()
            for dst in srcs:

                if src.owner == dst.owner:
                    continue
                score, action = Action(self, src, dst).calc()
                if max_score is None or score > max_score:
                    max_score = score
                    best_action = action
        return max_score, best_action

    def to_json(self):
        return dict(
            width=self.width, height=self.height, maps=self.maps, shapes=self.units
        )

    def __repr__(self):

        s = [
            f"hp0: {self.hp[0]}, hp1: {self.hp[1]}",
            [C.WALL_S] * (self.width + 1),
        ]
        for i, row in enumerate(self.grid):
            tmp = ["*"]
            for j, c in enumerate(row):
                tmp.append(c.view())
            tmp.append("*")
            s.append(tmp)
        s.append([C.WALL_S] * (self.width + 1))
        return "\n".join(["".join(r) for r in s])
