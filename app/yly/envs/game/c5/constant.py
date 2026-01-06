from common.algo.base.bin_util import encode_data, decode_data, set_mask
from common.util.export import List, Dict, defaultdict, logger, log


class ConstantC5:
    STATE_NULL = 0
    STATE_FIRST = 1
    STATE_SECONED = 2
    BIT_SIZE = 2
    CHESS_SIZE = 2
    DR = [[0, 1], [1, 0], [1, 1], [1, -1]]

    def init_mask_state(self):
        self.max_state = (1 << (2 * self.in_row)) - 1
        self.mask_state = [0] * self.max_state
        self.line_ct = {i: 0 for i in range(-self.in_row - 1, self.in_row + 2)}
        for mk in range(self.max_state):
            mask = mk
            ct = [0, 0, 0, 0]
            for _ in range(self.in_row):
                ct[mask & 3] += 1
                mask = mask >> 2
            if ct[3]:
                continue
            if ct[1] == 0 and ct[2]:
                self.mask_state[mk] = -ct[2]
            if ct[2] == 0 and ct[1]:
                self.mask_state[mk] = ct[1]
            # if ct[1] == 1 and ct[2] == self.in_row - 1:
            #     self.mask_state[mk] = self.op_win_state
            # if ct[2] == 1 and ct[1] == self.in_row - 1:
            #     self.mask_state[mk] = -self.op_win_state
        self.score = dict()

    def load(self, width=6, height=6, in_row=4):
        self.width = width
        self.height = height
        self.in_row = in_row
        self.op_win_state = self.in_row + 1  #
        self.init_size()
        self.init_mask()
        self.init_mask_state()
        self.init_lines()
        return self

    def init_size(self):
        self.size = self.width * self.height

    def init_mask(self):
        self.row_bit = self.BIT_SIZE * self.width
        self.height_bit = self.BIT_SIZE * self.height
        self.mask_cloumn = (1 << self.height_bit) - 1
        self.mask_row = (1 << self.row_bit) - 1
        self.mask_bit = (1 << self.BIT_SIZE) - 1
        self.grid = [self.STATE_NULL] * self.size
        self.pos_status: Dict[int, set] = {
            self.STATE_NULL: set(range(self.size)),
            self.STATE_FIRST: set(),
            self.STATE_SECONED: set(),
        }
        self.state = 0
        return self

    def init_lines(self):
        self.lines = [[] for _ in range(self.size)]
        self.line_pos = []
        self.line_state = []

        for i in range(self.size):
            l1, l2 = self.get_l(i)
            for dy, dx in self.DR:
                poss = []
                for k in range(self.in_row):
                    idx = self.get_dis(l1, l2, dy, dx, k)
                    if idx is None:
                        continue
                    poss.append([idx, k])
                if len(poss) != self.in_row:
                    continue
                line_id = len(self.line_state)
                self.line_pos.append(poss)
                for j, k in poss:
                    self.lines[j].append([line_id, k])
                self.line_state.append(0)

    def get_move_obs(self, idx, player_id):
        obs = dict()
        for lid, pos in self.lines[idx]:
            old_state = self.line_state[lid]
            new_state = set_mask(
                old_state, pos * self.CHESS_SIZE, self.CHESS_SIZE, player_id
            )
            old_statu, new_statu = (
                self.mask_state[old_state],
                self.mask_state[new_state],
            )
            if old_statu:
                obs[old_statu] = obs.get(old_statu, 0) - 1
            if new_statu:
                obs[new_statu] = obs.get(new_statu, 0) + 1
        return obs

    def game_over(self):
        from .state import State

        depth = self.state.bit_count()
        player_id = depth % 2
        for s in self.line_state:
            if player_id == 0 and s == C.in_row - 1:
                return State.FIRST_WIN, player_id, depth
            if player_id == 1 and s == -C.in_row + 1:
                return State.SECONEND_WIN, player_id, depth
        if depth == self.size:
            return State.NO_WIN, player_id, depth
        return False, player_id, depth

    def get_line_ct(self):
        return {k: v for k, v in self.line_ct.items() if v > 0}

    def change_chess_statu(self, idx, player_id):
        self.pos_status[player_id].add(idx)
        self.pos_status[self.grid[idx]].remove(idx)
        # logger.map(idx=idx, cid=self.grid[idx], newid=player_id)
        for lid, pos in self.lines[idx]:
            old_state = self.line_state[lid]
            self.line_state[lid] = set_mask(
                self.line_state[lid], pos * self.CHESS_SIZE, self.CHESS_SIZE, player_id
            )
            s1, s2 = self.mask_state[old_state], self.mask_state[self.line_state[lid]]
            self.line_ct[s1] -= 1
            self.line_ct[s2] += 1
            # ps = [[[v[0] // self.width, v[0] % self.width] for v in self.line_pos[lid]]]
            # if abs(s1) == self.in_row + 1:
            #     log.debug(f"LOS pos={ps} o:{s1} n:{self.line_ct[s1]}")
            # if abs(s2) == self.in_row + 1:
            #     log.debug(f"NEW pos={ps} o:{s2} n:{self.line_ct[s2]}")
        self.grid[idx] = player_id
        # log.debug("\n".join(self.to_str()))

    def get_next_state(self, idx, player_id):
        return self.get_move_obs(idx, player_id), set_mask(
            self.state, idx * self.CHESS_SIZE, self.CHESS_SIZE, player_id
        )

    def set_state(self, state: int):
        if self.state == state:
            return self
        self.change_mask(state)
        return self

    # set_state = set_mask

    def change_mask(self, state):
        state1, state2 = self.state, state
        for l1 in range(self.get_loop1()):
            state3, state4 = state1 & self.mask_cloumn, state2 & self.mask_cloumn
            state1 = state1 >> self.row_bit
            state2 = state2 >> self.row_bit

            if state3 == state4:
                continue
            self.change_col(l1, state3, state4)
        self.state = state
        return self

    def get_loop1(self):
        return self.height

    def get_loop2(self):
        return self.width

    def get_dis(self, l1, l2, dy, dx, k):
        l3, l4 = dy * k + l1, dx * k + l2
        if not self.is_valide_pos(l3, l4):
            return None
        return self.get_idx(l3, l4)

    def is_valide_pos(self, l3, l4):
        return 0 <= l3 < self.get_loop1() and 0 <= l4 < self.get_loop2()

    def change_col(self, l1, state3: int, state4: int):
        for l2 in range(self.get_loop2()):
            player_id = state4 & self.mask_bit
            self.set_pos_player_id(self.get_idx(l1, l2), player_id)
            state4 = state4 >> self.BIT_SIZE

    def set_pos_player_id(self, idx, player_id):
        if self.grid[idx] != player_id:
            # self.update_move_obs(idx, player_id)
            self.change_chess_statu(idx, player_id)
            # logger.map(idx=idx, player_id=player_id)

    def get_l(self, i):
        return i // self.get_loop2(), i % self.get_loop2()

    def get_yx(self, i):
        return i // self.get_loop2(), i % self.get_loop2()

    def get_idx(self, l1, l2):
        return l1 * self.get_loop2() + l2

    def s(self, v):
        return ["-", "O", "X"][v]

    def to_str(self):
        ret = [[f"{i}"] + [" "] * self.width for i in range(self.size // self.width)]
        for i, v in enumerate(self.grid):
            y, x = self.get_yx(i)
            ret[y][x + 1] = self.s(v)
        ret.append([" "] + [str(v) for v in range(self.width)])
        ret.append([str(self.get_line_ct())])
        return [" ".join(row) for row in ret]


C = ConstantC5()
CS = ConstantC5()


def load(w, h, in_row):
    C.load(w, h, in_row)
    CS.load(w, h, in_row)
