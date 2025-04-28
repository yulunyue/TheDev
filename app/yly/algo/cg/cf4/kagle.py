from app.yly.algo.cg.cf4.constant import C, S, logger
from app.yly.algo.cg.cf4.states.f4action import F4Action
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

    def evaluate_cell(self, state):
        return 0

    def calculate_points(self, state):
        pass

    def evaluate_pattern(self):
        pass

    def explore_cell_above(self, cell):
        pass

    def get_pattern(self, x, x_fun, y, y_fun, cells_remained):
        pass

    def choose_best_cell(self, best_state, current_state):
        pass

    def search_main(self, state: F4Action, **kw):
        a: F4Action = state.dst.get_random_action()
        state.dst.best_action = a
        # state.dst.best_action = self.evaluate_cell(state.dst)

    def __call__(self, env: KaggleEnv, conf: KaggleEnv):
        return super().search(*args).action


class KagleAgent(Algo):

    def search_main(self, state: F4Action, **kw):
        from app.yly.algo.kagle.c4 import cell_swarm1

        obs = KaggleEnv(
            state.dst.get_grid(), C.HEIGHT, C.WIDTH, state.dst.player_id + 1
        )
        action, grid = cell_swarm1(obs, obs)
        state.dst.best_action = state.dst.get_action(action)

    def __call__(self, *args, **kwds):
        from app.yly.algo.kagle.c4 import cell_swarm

        return cell_swarm(*args, **kwds)
