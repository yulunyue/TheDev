from app.yly.game.envs.cw.model.shape import ShapeBase
from app.yly.game.envs.cw.model.constant import C
from app.yly.game.envs.cw.model.action import CwAction
from common.util.export import List, Dict, logger
import random
from .path import Path
from common.algo.search.state import State


class World(State):
    maps = None
    show_msgs = []

    def __init__(self, state: str, player_id):
        super().__init__(state, player_id)
        maps, *args = state.split("|")
        self.load(maps)
        if args:
            self.set_shapes(args[0])

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

    def set_shapes(self, shapes: str):
        self.cultists: List[Dict[int, ShapeBase]] = [dict(), dict(), dict()]
        self.hp = [0, 0, 0]
        self.shapes = shapes
        for s in self.null_shapes:
            s.reset()
        shapes_int = [[int(v) for v in s.split(" ")] for s in shapes.split(",")]
        nodes: List[ShapeBase] = []
        for unit_id, unit_type, hp, x, y, owner in shapes_int:
            s = self.grid[y][x]
            nodes.append(s)
            s.load(unit_id, unit_type, hp, x, y, owner)
            self.cultists[owner][unit_id] = s
            self.hp[owner] += hp
        for s in nodes:
            s.bfs_find_action()
        return self

    def get_actions(self, depth=1, **kw):
        self.actions: Dict[str, CwAction] = dict()

        def add_action(src, method, dst):
            if dst is None:
                return

            a = CwAction(self, src, method, dst, self)
            if a.reward is None:
                return
            self.actions[a.action] = a

        for src in self.cultists[self.player_id].values():
            for dst in src.get_nexts_tiles():
                if dst.unit_type == C.TYPE_NULL:
                    add_action(src, C.ACTION_MOVE, dst)
                elif (
                    dst.unit_type == C.TYPE_CULTIST
                    and dst.owner == C.OWNER_NEUTRAL
                    and src.unit_type == C.TYPE_CULT_LEADER
                ):
                    add_action(src, C.ACTION_CONVERT, dst)
            if src.unit_type == C.TYPE_CULTIST:
                add_action(src, C.ACTION_SHOOT, src.path.get_near(1 - self.player_id))
                add_action(src, C.ACTION_SHOOT, src.path.leaders[1 - self.player_id])
        return self.actions

    def to_json(self):
        return dict(state=f"{self.maps}|{self.shapes}")

    def to_str(self):

        s = self.show_msgs + [
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

    def get_reward(self, actions: List[CwAction], **kw):
        return 0
