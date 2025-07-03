from app.yly.algo.cg.cf4.constant import C, S, logger
from app.yly.algo.cg.cf4.cf4action import F4Action
from app.yly.algo.cg.cf4.cf4state import F4State
from common.algo.search.algo import Algo
from typing import List
from app.yly.algo.cg.cf4.c4_mul import cell_swarm1, cell_swarm


def row_point_fmt(pts):
    return ",".join(
        ["".join([str(v) for v in pts[i : i + 6]]) for i in range(0, len(pts), 6)]
    )


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

    def search_main(self, state: F4State, **kw):

        actions: List[F4Action] = list(state.get_actions().values())
        state.best_action = None
        max_reward = None
        obs = KaggleEnv(
            C.mask_to_grid(state.state), C.HEIGHT, C.WIDTH, state.player_id + 1
        )
        action, grid = cell_swarm1(obs, obs)
        info2 = []
        for a in actions:
            reward, ptsrc = a.get_reward_by_c4()
            if max_reward is None or reward > max_reward:
                max_reward = reward
                state.best_action = a
            row = grid[a.action]
            # pt2 = row_point_fmt(row[state.row_idx[a.action]]["points"])
            # r2 = row_point_fmt(reward[:-1])
            pt2 = row_point_fmt(row[state.row_idx[a.action]]["pts"])
            r2 = row_point_fmt(ptsrc)
            if pt2 != r2:
                info2.append(f"points_diff{a.action}:\nY:{pt2}\nN:{r2}")

        state.best_action.set_info(info2)
        return state.best_action

    def __call__(self, env: KaggleEnv, conf: KaggleEnv):
        return super().search(env.board).action


class KagleAgent(Algo):
    def search_main(self, state: F4State, **kw):

        obs = KaggleEnv(
            C.mask_to_grid(state.state), C.HEIGHT, C.WIDTH, state.player_id + 1
        )
        action, grid = cell_swarm1(obs, obs)

        state.best_action = state.get_action(action)
        info2 = []
        # info = grid[action][state.row_idx[action]]
        # for name in ["swarm_patterns", "opp_patterns"]:
        #     for key, values in info[name].items():
        #         s2 = f"{name}_{key}:  "
        #         for v in values:
        #             s2 += ("?" + S)[v["mark"]]
        #         info2.append(s2)
        for i, row in enumerate(grid):
            info2.append(f"points{i}:{row[state.row_idx[i]]['points']}")
        state.set_info(info2)

    def __call__(self, *args, **kwds):

        return cell_swarm(*args, **kwds)
