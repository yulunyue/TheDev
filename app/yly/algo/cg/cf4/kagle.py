from app.yly.algo.cg.cf4.constant import C
from app.yly.algo.cg.cf4.f4state import F4State
from common.algo.search.algo import Algo


class Kagle(Algo):
    def evaluate_cell(self, state: F4State):
        pattern = self.get_pattern(state)
        points = self.calculate_points(pattern)

    def get_pattern(self, x, x_fun, y, y_fun, cells_remained):
        pattern = []
        x = x_fun(x)
        y = y_fun(y)

        return pattern

    def get_patterns(self, state: F4State):
        pass

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

    def search_main(self, state: F4State, **kw):
        current_action = self.evaluate_cell(state)
        state.best_action = self.choose_best_cell(state.best_action, current_action)
