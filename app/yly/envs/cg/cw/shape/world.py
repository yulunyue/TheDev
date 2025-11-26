from .cell import ShapeBase
from ..model.constant import C
from common.util.export import List, Dict, logger, defaultdict
import random


from .b_line_help import BM


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
        self.init_can_shoot_flag = defaultdict(bool)
        for i in range(self.height):
            tmp = []
            for j in range(self.width):
                s = ShapeBase(maps[i][j], i, j)
                if s.shape_type == C.TYPE_NULL:
                    self.null_shapes.append(s.reset())
                tmp.append(s)
            self.grid.append(tmp)
        for s in self.null_shapes:
            self.init_path(s)
        return self

    def load_shapes(self, shapes: List[List[int]]):
        for s in self.null_shapes:
            s.reset()
        self.nodes: List[ShapeBase] = [None] * 16
        self.hp = [0, 0, 0]
        self.owner = [0, 0, 0]
        self.leaders: List[ShapeBase] = [None] * 2
        self.cultists: List[Dict[int, ShapeBase]] = [dict(), dict(), dict()]
        self.can_shoot_flag = self.init_can_shoot_flag.copy()
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
            for src, dst in self.in_shot_way[s.k]:
                self.can_shoot_flag[src.k, dst.k] = False
        return self

    def init_path(self, s):
        self.in_shot_way: Dict[str, List[ShapeBase]] = defaultdict(list)
        self.bfs(s, self.init_min_path)

    def init_min_path(self, src: ShapeBase, dst: ShapeBase, path: List[ShapeBase]):
        # logger.map(src=src.k, dst=dst.k, l=len(path))
        src.min_step[dst.k] = len(path)
        if len(path) < C.VALUE_DAMAGE_MAX:
            self.init_shoot_path(src, dst)
        return True

    def init_shoot_path(self, src: ShapeBase, dst: ShapeBase):
        paths: List[ShapeBase] = []
        for dy, dx in BM.get(dst.y - src.y, dst.x - src.x):
            y, x = src.y + dy, src.x + dx
            t = self.grid[y][x]
            if t.shape_type == C.TYPE_OBS:
                paths = []
                break
            paths.append(t)
        self.init_can_shoot_flag[src.k, dst.k] = len(paths) != 0
        for t in paths:
            # if src.k == (5, 7) and dst.k == (3, 4):
            #     logger.map(src=src.k, dst=dst.k, mid=t.k)
            self.in_shot_way[t.k].append([src, dst])

    def bfs(self, s1: ShapeBase, call):
        q: List[ShapeBase] = [s1]
        vt = {s1.k: []}
        while q:
            tmp, q = q, []
            for t in tmp:
                for p in t.get_nexts_tiles():
                    if p.k in vt:
                        continue
                    vt[p.k] = vt[t.k] + [p]
                    if call(s1, p, vt[p.k]):
                        q.append(p)


ENV = World()
