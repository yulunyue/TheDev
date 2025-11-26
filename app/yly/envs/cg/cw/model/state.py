from common.algo.search.state import State, Action
from ..shape.world import World, C, ENV
from common.util.export import logger


class CwState(State):
    def __init__(self, state: str):
        self.state = state
        self.board = [[int(s) for s in v.split()] for v in state.split(",")]
        ENV.load_shapes(self.board)
        self.player_id = 0

    def make_actions(self):

        from .action import CwAction

        actions = []
        cultists = list(ENV.cultists[self.player_id].values())
        if ENV.leaders[self.player_id]:
            cultists += [ENV.leaders[self.player_id]]
        op_cultists = list(ENV.cultists[1 - self.player_id].values())
        if ENV.leaders[1 - self.player_id]:
            op_cultists += [ENV.leaders[1 - self.player_id]]
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
                for dst in op_cultists:
                    if src.min_step[dst.k] >= C.VALUE_DAMAGE_MAX:
                        continue
                    # logger.map(
                    #     s=src.view(),
                    #     ps=src.k,
                    #     d=dst.view(),
                    #     ds=dst.k,
                    #     d1=src.min_step[dst.k],
                    #     d2=src.get_abs_dis(dst),
                    # )
                    if ENV.can_shoot_flag[src.k, dst.k]:
                        actions.append(
                            CwAction(
                                self,
                                src,
                                C.ACTION_SHOOT,
                                dst,
                                C.VALUE_DAMAGE_MAX - src.get_abs_dis(dst),
                            )
                        )

        return actions

    def to_str(self):
        s = [
            " " + "".join(["%02d" % i for i in range(ENV.width)]),
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
        s.extend([a.show() for a in actions])
        return s
