from .cell import ShapeBase
from ..model.constant import C
from ..model.action import CwAction
from common.util.export import List, Dict, logger
import random
from .path import Path


class World:
    maps = None
    show_msgs = []

    def __init__(self, maps: str):
        self.load(maps)
        self.load_shapes()

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
                s = ShapeBase(self, maps[i][j]).load(None, maps[i][j], None, j, i, None)
                if s.shape_type == C.TYPE_NULL:
                    self.null_shapes.append(s)
                tmp.append(s)
            self.grid.append(tmp)
        return self

    def set_shapes(self, shapes):
        self.cultists: List[Dict[int, ShapeBase]] = [dict(), dict(), dict()]
        unit_id = 1
        for owner in range(C.PLAYER_NUM):
            s = ShapeBase(self, C.TYPE_NULL)
            s.load(unit_id, C.TYPE_CULT_LEADER, C.DEFAULT_HP, -1, -1, owner)
            self.cultists[owner][unit_id] = s
            unit_id += 1
        for _ in range(C.UNITS_CULTIST_NUM):
            ShapeBase(self, C.TYPE_NULL).load(
                unit_id, C.TYPE_CULTIST, C.DEFAULT_HP, -1, -1
            )
            unit_id += 1
            self.cultists[C.OWNER_NEUTRAL][unit_id] = s
        return self

    def get_sort_actions(self, **kw):
        actions = []

        for src in self.cultists[self.player_id].values():
            for dst in src.get_nexts_tiles():
                if dst.unit_type == C.TYPE_NULL:
                    actions.append(CwAction(src, C.ACTION_MOVE, dst))
                elif (
                    dst.unit_type == C.TYPE_CULTIST
                    and dst.owner == C.OWNER_NEUTRAL
                    and src.unit_type == C.TYPE_CULT_LEADER
                ):
                    actions.append(CwAction(src, C.ACTION_CONVERT, dst))
            if src.unit_type == C.TYPE_CULTIST:
                near_cul = src.path.get_near(1 - self.player_id)
                if src.can_shoot(near_cul):
                    actions.append(CwAction(src, C.ACTION_SHOOT, near_cul))
                if src.can_shoot(src.path.leaders[1 - self.player_id]):
                    actions.append(
                        CwAction(
                            src, C.ACTION_SHOOT, src.path.leaders[1 - self.player_id]
                        )
                    )
        return actions
