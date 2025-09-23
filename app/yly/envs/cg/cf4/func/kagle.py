from common.algo.search.algo import Algo
from typing import List
from ..model.constant import C
from ..model.cf4state import F4State, F4Action
from .c4_mul import cell_swarm, cell_swarm1


class KaggleEnv:

    def __init__(self, board, rows, columns, mark):
        self.board = board
        self.rows = rows
        self.columns = columns
        self.mark = mark
        self.inarow = C.IN_ROW


class Kagle(Algo):
    """
    uri = https://www.kaggle.com/competitions/connectx/data
    """

    def search_main(self, state: F4State, **kw):
        obs = KaggleEnv(
            C.mask_to_grid(state.state), C.HEIGHT - 1, C.WIDTH, state.player_id + 1
        )
        cells = cell_swarm1(obs, obs)
        state.data = dict()
        for cell in cells:
            state.data[cell["x"]] = cell["points"]
        state.set_best_action(state.get_action(cells[0]["x"]))

    def __call__(self, env: KaggleEnv, conf: KaggleEnv):
        return cell_swarm(env, conf)
