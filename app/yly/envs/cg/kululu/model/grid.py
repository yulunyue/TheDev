from common.util.export import List, Dict, defaultdict
from .player import Player, C
from .shape import Shape
import json
from .kl_action import KlAction


class Grid:

    def load_from_json(self, mapes, **kw):
        self.load_map(mapes)
        return self

    def load_map(self, maps: List[str]):
        self.borads: List[List[Shape]] = []
        self.width = len(maps[0])
        self.height = len(maps)
        self.maps = maps
        null_shapes: List[Shape] = []
        for i, row in enumerate(maps):
            tmp = []
            for j, v in enumerate(row):
                s = Shape(i, j, v)
                if s.entity_type == C.TYPE_NULL:
                    null_shapes.append(s)
                tmp.append(s)
            self.borads.append(tmp)
        for d in null_shapes:
            d.set_grid(self)
        return self

    def get_actions(self, depth=1, **kw):
        wait_action = KlAction(self, C.ACTION_WAIT).set_reward(0)
        self.actions = {C.ACTION_WAIT: wait_action}
        for n in self.player.cell.get_nexts():
            k = f"{C.ACTION_MOVE} {n.y} {n.x}"
            self.actions[k] = KlAction(self, k).set_reward(1)
        return self.actions

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
            p = Player(*pargs).set_grid(self)
            if p.entity_type == C.EXPLORER:
                if p.key == "0":
                    self.player = p
                else:
                    self.explorer.append(p)
            elif p.entity_type == C.WANDERER:
                self.wanderer.append(p)
            self.nodes_list.append(Player(*pargs))
        self.state = json.dumps(self.dump())
        return self

    def dump(self):
        return dict(
            height=self.height,
            width=self.width,
            mapes=self.maps,
            players=[d.dump() for d in self.nodes_list],
        )

    def get_reward(self, *args, **kw):
        return 0
