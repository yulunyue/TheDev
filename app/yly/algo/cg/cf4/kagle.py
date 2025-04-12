from app.yly.algo.cg.cf4.constant import C, S
from app.yly.algo.cg.cf4.f4action import F4State, F4Action
from common.algo.search.algo import Algo


class Kagle(Algo):
    def evaluate_cell(self, state: F4State):
        return 0

    def calculate_points(self, state: F4State):
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
        state.dst.best_action = state.dst.get_random_action()
        # state.dst.best_action = self.evaluate_cell(state.dst)


class KagleAgent(Algo):

    def search_main(self, state: F4Action, **kw):
        from app.yly.algo.kagle.c4 import cell_swarm1

        action, grid = cell_swarm1(*state.dump_to_kaggle())
        a = state.dst.best_action = state.dst.get_action(action)
        info = grid[a.x][a.y]
        for k in ["swarm_patterns", "opp_patterns"]:
            for k1, v in info[k].items():
                info[k][k1] = "".join([("?" + S)[v1["mark"]] for v1 in v])
        state.dst.best_action.set_info(info)

    def __call__(self, *args, **kwds):
        from app.yly.algo.kagle.c4 import cell_swarm

        return cell_swarm(*args, **kwds)
