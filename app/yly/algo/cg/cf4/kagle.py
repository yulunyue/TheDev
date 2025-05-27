from app.yly.algo.cg.cf4.constant import C, S, logger
from app.yly.algo.cg.cf4.cf4action import F4Action
from app.yly.algo.cg.cf4.cf4state import F4State
from common.algo.search.algo import Algo


class KaggleEnv:

    def __init__(self, board, rows, columns, mark):
        self.board = board
        self.rows = rows
        self.columns = columns
        self.mark = mark
        self.inarow = C.inarow


class Kagle(Algo):
    """
    uri = https://www.kaggle.com/competitions/connectx/data
    """

    def search_main(self, state: F4Action, **kw):
        best_action: F4Action = None
        for k, a in state.dst.get_actions().items():
            if best_action is None:
                best_action = a
            if a.dst.points > best_action.dst.points:
                best_action = a
            elif (
                a.dst.points == best_action.dst.points
                and C.WIDTH_POINTS[best_action.action] < C.WIDTH_POINTS[k]
            ):
                best_action = a

        state.dst.best_action = best_action

    def __call__(self, env: KaggleEnv, conf: KaggleEnv):
        return super().search(env.board).action


class KagleAgent(Algo):

    def search_main(self, state: F4Action, **kw):
        from app.yly.algo.cg.cf4.kagle_c4 import cell_swarm1

        obs = KaggleEnv(
            state.dst.get_grid(), C.HEIGHT, C.WIDTH, state.dst.player_id + 1
        )
        action, grid = cell_swarm1(obs, obs)

        state.dst.best_action = state.dst.get_action(action)
        info = grid[action][state.dst.row_idx[action]]
        info1 = None
        if state.dst.row_idx[action] >= 1:
            info1 = grid[action][state.dst.row_idx[action] - 1]
        info2 = ""
        for name in ["swarm_patterns", "opp_patterns"]:
            for key, values in info[name].items():
                s2 = f"{name}_{key}:  "
                for v in values:
                    s2 += ("?" + S)[v["mark"]]
                info2 += s2 + "\n"

        point_sw = info["points"]
        point_sl = state.dst.best_action.dst.points

    #         state.dst.best_action.set_info(
    #             f"""
    # point_sw0:{info["pts"]},
    # point_sw1:{info1["pts"] if info1 else None}
    # point_sw:{point_sw}
    # point_sl:{point_sl}
    # msg:RSW{point_sw==point_sl}
    # info2:\n{info2}"""
    #         )

    def __call__(self, *args, **kwds):
        from app.yly.algo.cg.cf4.kagle_c4 import cell_swarm

        return cell_swarm(*args, **kwds)
