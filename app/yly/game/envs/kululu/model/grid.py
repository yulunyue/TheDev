from common.util.export import List
from app.yly.game.envs.kululu.model.player import Player, C, Shape
from common.algo.base.graph import Graph
from common.algo.base.math_util import math, mean
import json


class Grid:
    g: Graph = None

    def __init__(self):
        self.node_map = {"#": [], ".": [], "w": []}

    def load_from_json(self, width, height, mapes, players, **kw):
        self.load_size(width, height)
        self.load_map(mapes)
        self.set_players(players)
        return self

    def load_size(self, width, height):
        self.width = width
        self.height = height
        return self

    def load_map(self, maps: List[str]):
        if self.g:
            return
        self.src_map = maps
        self.maps: List[List[Shape]] = []
        self.board_show = []
        self.g = Graph().reset()
        for i, row in enumerate(maps):
            tmp = []
            self.board_show.append([])
            for j, v in enumerate(row):
                s = Shape(i, j, v, len(self.node_map[v]))
                self.node_map[v].append(s)
                tmp.append(s)
                self.board_show[-1].append(s.view())
                for dy, dx in C.DR:
                    y, x = i + dy, j + dx
                    if y < 0 or x < 0 or y >= self.height or x >= self.width:
                        continue
                    if maps[y][x] == "#":
                        continue
                    self.g.add_edge((i, j), (y, x))
                    self.g.add_edge((y, x), (i, j))
            self.maps.append(tmp)
        self.null_pos: List[Shape] = self.node_map["."]
        for n in self.g.nodes.values():
            n.bfs()

    def get_action(self):
        min_e_dis = None
        rt = None
        for key in self.g.nodes[self.player.pos].childs:
            min_w_dis = self.calc_w(key)
            if min_w_dis < 2:
                continue
            e_dis = self.calc_e(key)
            if min_e_dis is None or e_dis < min_e_dis:
                min_e_dis = e_dis
                rt = key
        return rt

    def calc_e(self, pos):
        es = []
        for e in self.explorer:
            es.append(self.g.get_dis(pos, e.pos))
        return mean(es)

    def calc_w(self, pos):
        dis = float("inf")
        for w in self.wanderer:
            d = self.g.get_dis(pos, w.pos)
            if d < dis:
                dis = d
        return dis

    def load_param(self, args):
        (
            self.sanity_loss_lonely,
            self.sanity_loss_group,
            self.wanderer_spawn_time,
            self.wanderer_life_time,
        ) = args

    def set_players(self, ps):
        self.explorer: List[Player] = []
        self.nodes_list: List[Player] = []
        self.wanderer: List[Player] = []
        for pargs in ps:
            p = Player(*pargs)
            if p.entity_type == C.EXPLORER:
                if p.key == "0":
                    self.player = p
                else:
                    self.explorer.append(p)
            elif p.entity_type == C.WANDERER:
                self.wanderer.append(p)
            self.nodes_list.append(Player(*pargs))

    def dump(self):
        return dict(
            height=self.height,
            width=self.width,
            mapes=self.src_map,
            players=[d.dump() for d in self.nodes_list],
        )

    def __repr__(self):
        board_row = json.loads(json.dumps(self.board_show))
        for p in self.nodes_list:
            board_row[p.y][p.x] = p.view()
        # for p in self.null_pos:
        #     board_row[p.y][p.x] = "%02d" % self.g.get_dis(p.pos, self.explorer[0].pos)
        return "\n".join(["".join(rows) for rows in board_row])
