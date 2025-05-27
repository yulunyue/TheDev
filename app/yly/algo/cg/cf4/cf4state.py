from app.yly.algo.cg.cf4.constant import C, DR
from common.algo.export import State


class F4State(State):
    def __init__(self, state):
        super().__init__(state, player_id=0, depth=0)

    @classmethod
    def new_state(cls, key):
        a: F4State = super().new_state(key)
        return a.load_root()

    @classmethod
    def get_init_state(cls):
        return cls.new_state(C.grid_to_mask([0] * (C.WIDTH * C.HEIGHT)))

    def get_mask(self):
        grid = self.get_grid()
        return C.grid_to_mask(grid)

    def to_str(self):
        return (
            "\n"
            + "\n".join(
                [
                    f"done:{self.done},depth:{self.depth}",
                    f"mask:{self.get_mask()}",
                    C.grid_view(self.get_grid()),
                ]
            )
            + "\n"
        )

    def __str__(self):
        return self.to_str()

    def load_root(self):
        # self.grid: list = [0] * (C.WIDTH * C.HEIGHT)
        if isinstance(self.state, list):
            self.row_idx, self.can_move, self.line_state, self.player_id, self.depth = (
                C.grid_to_line_state(self.state)
            )
        elif isinstance(self.state, int):
            self.row_idx, self.can_move, self.line_state, self.player_id, self.depth = (
                C.mask_to_line_state(self.state)
            )
        else:
            raise Exception("gg")
        return self

    def get_action(self, x):
        from app.yly.algo.cg.cf4.cf4action import F4Action

        line_state = self.line_state.copy()
        # load_from_parent(x, self)
        return F4Action(self, self.row_idx[x], x, F4State.new_state())

    def get_actions_all(self):
        return self.can_move

    def load_from_parent(self, x, p: "F4State"):
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
        self.update_points(k, p.player_id)
        self.update_states(k, p.player_id)
        if self.points[0]:
            self.done = p.player_id
        return self

    def update_points(self, k, player_id):
        """
        POINTS: A04,B04,-B14,-A14,xn(A03,B03),xn(A02,B02),-xn(A12,B12)
        """
        self.points = []
        op = 1
        for i in range(C.HEIGHT):
            if k - i * C.WIDTH >= 0:
                points = self.get_action_points(k - i * C.WIDTH, player_id)
                if i == 1:
                    self.points[2:2] = [op * points[1], op * points[0]]
                    if abs(self.points[4]) < min(points[2], 2):
                        self.points[4:4] = [op * points[2]]
                        if abs(self.points[5]) < min(points[3], 2):
                            self.points[5:5] = [op * points[3]]
                        else:
                            self.points[7:7] = [op * points[3]]
                    else:
                        self.points[6:6] = [op * points[2], op * points[3]]
                    self.points.extend([v * op for v in points[4:]])
                else:
                    self.points.extend([v * op for v in points])
                # if i <= 1:

                #     self._info += f"point_sl{i}:{points}\n"
            else:
                self.points.extend([0] * 6)
            op *= -1
        return self

    def update_states(self, i, player_id):
        for line_id, l, idx in C.point_line_id[i]:
            self.line_state[line_id] |= [1, 2][player_id] << (2 * idx)

    def get_action_points(self, i, player_id):
        """
        POINT0: A4,A3,A2
        POINT1: B4,B3,B2
        POINTS: A4,B4,xn(A3,B3),xn(A2,B2)
        """
        dr_ct = [[0] * len(DR) for _ in range(2)]
        points = [0] * 6
        for line_id, l, idx in C.point_line_id[i]:
            ct0, ct1, _ = C.scores[self.line_state[line_id]]
            # self._info += f"line:{C.lines[line_id]},l:{[l,ct0,ct1]},state:{C.line_fmt(self.line_state[line_id])}\n"
            if ct1 == 0 and ct0 > dr_ct[player_id][l]:
                dr_ct[player_id][l] = ct0
            if ct0 == 0 and ct1 > dr_ct[1 - player_id][l]:
                dr_ct[1 - player_id][l] = ct1
        # self._info += f"dr_ct:{dr_ct}"
        for j in range(2):
            for i in range(len(DR)):
                for k in range(1, dr_ct[j][i] + 1):
                    points[(3 - k) * 2 + j] += 1
        for i, j in [[2, 3], [4, 5]]:
            if points[i] < points[j]:
                points[i], points[j] = points[j], points[i]

        return points

    def get_grid(self):
        ret = []
        for v in C.point_line_id:
            line_id, l, idx = v[0]
            state = (self.line_state[line_id] >> (idx * 2)) & 3
            ret.append(state)

        return ret

    _info = ""

    def get_info(self):
        return self._info


def get_state(state):
    if isinstance(state, F4State):
        return state
    return F4State().load_root(state=state)
