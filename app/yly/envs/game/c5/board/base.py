from common.algo.base.bin_util import encode_data, decode_data, set_mask
from common.util.export import List, Dict, defaultdict, logger, log


class BoardC5:
    STATE_NULL = 0
    STATE_FIRST = 1
    STATE_SECONED = 2
    BIT_SIZE = 2
    CHESS_SIZE = 2
    DR = [[0, 1], [1, 0], [1, 1], [1, -1]]

    def load(self, width=6, height=6, in_row=4):
        self.width = width
        self.height = height
        self.in_row = in_row
        self.init_size()
        self.init_mask()
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
        self.can_use = set(range(self.size))
        self.state = None
        return self

    def change_chess_statu(self, idx, player_id):

        # log.map(idx=idx, player_id=player_id)
        # if self.grid[idx] == player_id:
        #     raise Exception("xxx")
        if player_id == 0:
            self.can_use.add(idx)
        elif self.grid[idx] == 0 and player_id:
            self.can_use.remove(idx)
        self.grid[idx] = player_id

    def put_chess(self, idx, player_id):
        ct = defaultdict(int)
        for i in range(len(self.DR)):
            lv, l0 = self.get_dirction_ct(idx, i, player_id, -1, self.in_row)
            rv, r0 = self.get_dirction_ct(idx, i, player_id, 1, self.in_row - lv - l0)
            if lv + rv + l0 + r0 + 1 >= self.in_row:
                ct[
                    lv + rv + 1, 1 if l0 + r0 else 0
                ] += 1  # l0 + r0不等于1 表示两个方向都有可能
        self.change_chess_statu(idx, player_id)
        return ct

    def get_dirction_ct(self, idx, i, player_id, chen, size):
        c0 = cv = 0
        ct = 1
        has_op = 0
        while ct < size:
            nx = self.get_next_pos(idx, i, ct * chen)
            if nx is None or has_op:
                break
            if self.grid[nx] == 3 - player_id:
                has_op = 1
            if self.grid[nx] == player_id:
                cv += 1
            if self.grid[nx] == self.STATE_NULL:
                c0 += 1
            ct += 1
        return cv, c0

    def get_next_state(self, state, idx, player_id):
        return set_mask(state, idx * self.CHESS_SIZE, self.CHESS_SIZE, player_id + 1)

    def set_state(self, state: int):
        if self.state == state:
            return self
        if isinstance(state, int):
            self.change_mask(state)
        elif state:
            self.change_grid(state)
        self.state = state
        return self

    def change_grid(self, s: str):
        self.grid = [self.STATE_NULL] * self.size
        for i, v in enumerate(s.split("|")):
            self.change_chess_statu(int(v), (i % 2) + 1)
        self.state = s

    def change_mask(self, state):
        state1, state2 = self.state, state
        for l1 in range(self.get_loop1()):
            state3, state4 = state1 & self.mask_cloumn, state2 & self.mask_cloumn
            state1 = state1 >> self.row_bit
            state2 = state2 >> self.row_bit

            if state3 == state4:
                continue
            self.change_col(l1, state3, state4)
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

    def get_next_pos(self, idx, i, k):
        y, x = self.get_yx(idx)
        return self.get_dis(y, x, self.DR[i][0], self.DR[i][1], k)

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

    def get_line_point(self, idx, dr):
        pass

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
        return [" ".join(row) for row in ret]

    def set_actions_str(self):
        return self
