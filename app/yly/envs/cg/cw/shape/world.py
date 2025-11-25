from .cell import ShapeBase
from ..model.constant import C
from common.util.export import List, Dict, logger
import random
from .path import Path


class World:
    maps = None
    show_msgs = []

    def load(self, maps: str):
        self.maps = maps
        maps = maps.split(",")
        self.width = len(maps[0])
        self.height = len(maps)
        self.grid: List[List[ShapeBase]] = []
        self.null_shapes: List[ShapeBase] = []

        for i in range(self.height):
            tmp = []
            for j in range(self.width):
                s = ShapeBase(self, maps[i][j], i, j)
                if s.shape_type == C.TYPE_NULL:
                    self.null_shapes.append(s)
                tmp.append(s)
            self.grid.append(tmp)
        return self

    def load_shapes(self, shapes: List[List[int]]):
        for s in self.null_shapes:
            s.reset()
        self.nodes: List[ShapeBase] = [None] * 16
        self.hp = [0, 0, 0]
        self.owner = [0, 0, 0]
        self.leaders: List[ShapeBase] = [None] * 2
        self.cultists: List[Dict[int, ShapeBase]] = [dict(), dict(), dict()]
        for unit_id, unit_type, hp, x, y, owner in shapes:
            if hp <= 0:
                continue

            self.owner[owner] += 1
            self.hp[owner] += hp
            s = self.nodes[unit_id] = self.grid[y][x]
            self.grid[y][x].load(unit_id, unit_type, hp, owner)
            if unit_type == C.TYPE_CULT_LEADER:
                self.leaders[owner] = s
            else:
                self.cultists[s.owner][unit_id] = s
        return self
