from common.util.export import List
from app.yly.game.envs.kululu.model.player import Player


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def load(self, maps: List[str]):
        pass

    def load_param(self, args):
        (
            self.sanity_loss_lonely,
            self.sanity_loss_group,
            self.wanderer_spawn_time,
            self.wanderer_life_time,
        ) = args

    def add_player(self, *args):
        p = Player(*args)
        self.nodes_list.append(p)
        self.node_map[p.entity_type].append(p)

    def reset(self):
        self.node_map = {
            Player.EXPLORER: [],
            Player.WANDERER: [],
        }
        self.nodes_list: List[Player] = []
        return self
