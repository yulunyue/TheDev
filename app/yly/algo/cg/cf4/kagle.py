from app.yly.algo.cg.cf4.constant import C, S, logger
from app.yly.algo.cg.cf4.cf4action import F4Action
from app.yly.algo.cg.cf4.cf4state import F4State
from common.algo.search.algo import Algo
from typing import List


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
        state.best_action = actions[0]
        max_reward = actions[0].get_reward_by_c4()
        for a in actions[1:]:
            reward = a.get_reward_by_c4()
            if reward > max_reward:
                max_reward = reward
                state.best_action = a
        return state.best_action

    def __call__(self, env: KaggleEnv, conf: KaggleEnv):
        return super().search(env.board).action


class KagleAgent(Algo):
    def search_main(self, state: F4State, **kw):
        from app.yly.algo.cg.cf4.c4_mul import cell_swarm1

        obs = KaggleEnv(
            C.mask_to_grid(state.state), C.HEIGHT, C.WIDTH, state.player_id + 1
        )
        action, grid = cell_swarm1(obs, obs)

        state.best_action = state.get_action(action)
        info = grid[action][state.row_idx[action]]
        info2 = ""
        for name in ["swarm_patterns", "opp_patterns"]:
            for key, values in info[name].items():
                s2 = f"{name}_{key}:  "
                for v in values:
                    s2 += ("?" + S)[v["mark"]]
                info2 += s2 + "\n"

    def __call__(self, *args, **kwds):
        from app.yly.algo.cg.cf4.c4_mul import cell_swarm

        return cell_swarm(*args, **kwds)
