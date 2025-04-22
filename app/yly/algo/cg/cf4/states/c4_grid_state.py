from app.yly.algo.cg.cf4.states.base_state import F4State, C


class C4GridState(F4State):
    def load_root(self):
        self.grid: list = [0] * (C.WIDTH * C.HEIGHT)
        self.row_idx: list = [0] * C.WIDTH

    def get_action(self, x):
        y = self.row_idx[x] + 1
        if y >= C.HEIGHT:
            return
        from app.yly.algo.cg.cf4.states.f4action import F4Action

        return F4Action(self, y, x, self.add_child(y, x))

    def add_child(self, y, x):
        r = C4GridState()
        r.depth += self.depth + 1
        r.player_id = (self.player_id + 1) % C.PLAYER_NUM
        r.grid = self.grid.copy()
        r.row_idx = self.row_idx.copy()
        r.row_idx[x] = y
        r.grid[y * C.WIDTH + x] = r.player_id + 1
        return r
