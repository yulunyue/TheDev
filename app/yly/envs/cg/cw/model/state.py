from common.algo.search.state import State, Action
from ..shape.world import World, C


class CwState(State):
    g: World = None

    def __init__(self, state: str):
        super().__init__(state)
        self.board = [[int(s) for s in v.split()] for v in state.split(",")]
        CwState.g.load_shapes(self.board)
        self.calc_reward(CwState.g)

    def calc_reward(self, g: World):
        self.reward = 0
        g.hp
        g.owner
        if g.leaders:
            pass

    @staticmethod
    def set_envi(s: str):
        CwState.g = World(s)

    def make_actions(self):
        actions = dict()
        from .action import CwAction

        def add_action(a: CwAction):
            actions[a.action] = a

        for src in CwState.g.cultists[self.player_id].values():
            for dst in src.get_nexts_tiles():
                if dst.unit_type == C.TYPE_NULL:
                    add_action(CwAction(self, src, C.ACTION_MOVE, dst))
                elif (
                    dst.unit_type == C.TYPE_CULTIST
                    and dst.owner == C.OWNER_NEUTRAL
                    and src.unit_type == C.TYPE_CULT_LEADER
                ):
                    add_action(CwAction(self, src, C.ACTION_CONVERT, dst))
            if src.unit_type == C.TYPE_CULTIST:
                for dis, d in src.path.can_shoot_units:
                    add_action(CwAction(self, src, C.ACTION_SHOOT, d, param0=dis))
        return actions

    def to_str(self):
        s = [
            [C.WALL_S] * (CwState.g.width + 1),
        ]
        for i, row in enumerate(CwState.g.grid):
            tmp = ["*"]
            for j, c in enumerate(row):
                tmp.append(c.view())
            tmp.append("*")
            s.append(tmp)
        s.append([C.WALL_S] * (CwState.g.width + 1))
        acs = [a.show() for a in self.get_actions().values()]
        return "\n".join(["".join(r) for r in s] + acs)


class CwStateDev(CwState):
    pass
