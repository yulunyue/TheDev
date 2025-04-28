from app.yly.algo.cg.cf4.states.base_state import F4State
from app.yly.algo.cg.cf4.constant import C, DR


class C4GridState(F4State):
    def load_root(self):
        # self.grid: list = [0] * (C.WIDTH * C.HEIGHT)
        self.row_idx: list = [0] * C.WIDTH
        self.can_move = set(range(C.WIDTH))
        self.line_state = [0] * len(C.lines)

    def get_action(self, x):
        from app.yly.algo.cg.cf4.states.f4action import F4Action

        return F4Action(
            self, self.row_idx[x], x, C4GridState().load_from_parent(x, self)
        )

    def get_actions_all(self):
        return self.can_move

    def load_from_parent(self, x, p: "C4GridState"):
        self.depth += p.depth + 1
        self.player_id = (p.player_id + 1) % C.PLAYER_NUM
        # self.grid = p.grid.copy()
        self.row_idx = p.row_idx.copy()
        k = (C.HEIGHT - self.row_idx[x] - 1) * C.WIDTH + x
        self.line_state = p.line_state.copy()
        self.can_move = p.can_move.copy()
        # self.grid[k] = self.player_id + 1
        self.row_idx[x] += 1
        if self.row_idx[x] == C.HEIGHT:
            self.can_move.remove(x)
        if len(self.can_move) == 0:
            self.done = -1
        self.init_action_state(k, p.player_id)
        return self

    def init_action_state(self, i, player_id):
        for line_id, l, idx in C.point_line_id[i]:
            self.line_state[line_id] |= [1, 3][player_id] << (2 * idx)

    def get_cnt(self, y, x, dy, dx, player_id):

        for i in range(C.inarow):
            pass

    def get_grid(self):
        ret = []
        for v in C.point_line_id:
            for line_id, l, idx in v:
                if idx == 0:
                    state = self.line_state[line_id] & 3
                    ret.append(state)
                    break
        return ret

    def get_info(self):
        return f""
