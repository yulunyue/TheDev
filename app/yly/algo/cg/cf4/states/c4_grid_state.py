from app.yly.algo.cg.cf4.states.base_state import F4State
from app.yly.algo.cg.cf4.constant import C, DR


class C4GridState(F4State):
    def load_root(self):
        # self.grid: list = [0] * (C.WIDTH * C.HEIGHT)
        self.row_idx: list = [C.HEIGHT - 1] * C.WIDTH
        self.can_move = set(range(C.WIDTH))
        self.line_state = [0] * len(C.lines)

    def get_action(self, x):
        from app.yly.algo.cg.cf4.states.f4action import F4Action

        return F4Action(
            self, self.row_idx[x], x, C4GridState().load_from_parent(x, self)
        )

    def get_actions_all(self):
        return self.can_move

    def get_info(self):
        return f"points:{self.points}"

    def load_from_parent(self, x, p: "C4GridState"):
        self.depth += p.depth + 1
        self.player_id = (p.player_id + 1) % C.PLAYER_NUM
        # self.grid = p.grid.copy()
        self.row_idx = p.row_idx.copy()
        k = self.row_idx[x] * C.WIDTH + x
        self.line_state = p.line_state.copy()
        self.can_move = p.can_move.copy()
        # self.grid[k] = self.player_id + 1
        self.row_idx[x] -= 1
        if self.row_idx[x] == -1:
            self.can_move.remove(x)
        if len(self.can_move) == 0:
            self.done = -1
        done, self.points = self.get_action_state(k, p.player_id)
        if done is not None:
            self.done = done
        return self

    def get_action_state(self, i, player_id):
        done = None
        dr_ct = [[0] * len(DR) for _ in range(2)]
        points = [0] * 6
        for line_id, l, idx in C.point_line_id[i]:
            ct0, ct1, _ = C.scores[self.line_state[line_id]]
            if ct1 == 0 and ct0 > dr_ct[0][l]:
                dr_ct[player_id][l] = ct0
                if ct0 == 3 and player_id == 0:
                    done = 0
            if ct0 == 0 and ct1 > dr_ct[1][l]:
                dr_ct[1 - player_id][l] = ct1
                if ct1 == 3 and player_id == 1:
                    done = 1
            self.line_state[line_id] |= [1, 2][player_id] << (2 * idx)
        for j in range(2):
            for i in range(len(DR)):
                for k in range(1, dr_ct[j][i] + 1):
                    points[(3 - k) * 2 + j] += 1
        for i, j in [[2, 3], [4, 5]]:
            if points[i] < points[j]:
                points[i], points[j] = points[j], points[i]

        return done, points

    def get_cnt(self, y, x, dy, dx, player_id):

        for i in range(C.inarow):
            pass

    def get_grid(self):
        ret = []
        for v in C.point_line_id:
            line_id, l, idx = v[0]
            state = (self.line_state[line_id] >> (idx * 2)) & 3
            ret.append(state)

        return ret
