from common.algo.search.state import State, Action
from ..shape.world import World, C

ENV = World()


class CwState(State):
    def __init__(self, state: str):
        self.state = state
        self.board = [[int(s) for s in v.split()] for v in state.split(",")]
        ENV.load_shapes(self.board)
        self.player_id = 0

    def calc_reward(self, g: World):
        self.reward = 0
        g.hp
        g.owner
        if g.leaders[self.player_id]:
            min_v, sum_v, max_v = g.leaders[self.player_id].calc_dis(
                g.cultists[C.OWNER_NEUTRAL].values()
            )
            self.reward += min_v * 0.2 + sum_v * 0.1 - max_v * 0.1

    def make_actions(self):

        from .action import CwAction

        actions = []
        cultists = list(ENV.cultists[self.player_id].values())
        if ENV.leaders[self.player_id]:
            cultists += [ENV.leaders[self.player_id]]
        for src in cultists:
            for dst in src.get_nexts_tiles():
                if dst.unit_type == C.TYPE_NULL:
                    actions.append(CwAction(self, src, C.ACTION_MOVE, dst))
                elif (
                    dst.unit_type == C.TYPE_CULTIST
                    and dst.owner == C.OWNER_NEUTRAL
                    and src.unit_type == C.TYPE_CULT_LEADER
                ):
                    actions.append(CwAction(self, src, C.ACTION_CONVERT, dst))
            if src.unit_type == C.TYPE_CULTIST:
                for d, dis in src.path.can_shoot_units:
                    actions.append(CwAction(self, src, C.ACTION_SHOOT, d, param0=dis))
        return actions

    def to_str(self):
        s = [
            C.WALL_S * (ENV.width + 1),
        ]
        for i, row in enumerate(ENV.grid):
            tmp = ["*"]
            for j, c in enumerate(row):
                tmp.append(c.view())
            tmp.append("*")
            s.append("".join(tmp))
        s.append(C.WALL_S * (ENV.width + 1))
        actions = sorted(
            self.get_sort_actions(), key=lambda a: a.get_reward(), reverse=True
        )
        # s = [str(v) for v in s]
        s.append(",".join([a.show() for a in actions]))
        return s
