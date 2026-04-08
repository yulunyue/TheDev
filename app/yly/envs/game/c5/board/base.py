from common.algo.base.bin_util import encode_data, decode_data, set_mask
from common.util.export import List, Dict, defaultdict, logger, log


class BoardC5:
    STATE_NULL = 0
    STATE_FIRST = 1
    STATE_SECONED = 2
    DR = [[0, 1], [1, 0], [1, 1], [1, -1]]

    def load(self, width=6, height=6, in_row=4):
        self.width = width
        self.height = height
        self.size = self.width * self.height
        self.in_row = in_row
        self.init_size()
        self.init_mask()
        return self

    def init_size(self):
        self.size = self.width * self.height

    def init_mask(self):
        self.mask_h = (1 << self.height) - 1
        self.mask_full = (1 << self.size) - 1
        self.set_state(0)
        return self

    def put_chess(self, idx, player_id):
        mask = 1 << idx
        if player_id == 0:
            self.state_pos ^= mask
            return self
        self.state_pos |= mask
        if player_id == 1:
            self.state_statu &= self.mask_full - mask
        else:
            self.state_statu |= mask
        return self

    def xx(self, idx, player_id):
        ct = defaultdict(int)
        for i in range(len(self.DR)):
            lv, l0 = self.get_dirction_ct(idx, i, player_id, -1, self.in_row)
            rv, r0 = self.get_dirction_ct(idx, i, player_id, 1, self.in_row - lv - l0)
            if lv + rv + l0 + r0 + 1 >= self.in_row:
                ct[
                    lv + rv + 1, 1 if l0 + r0 else 0
                ] += 1  # l0 + r0不等于1 表示两个方向都有可能
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

    def set_state_any(self, state):
        if isinstance(state, int):
            self.set_state(state)
        elif isinstance(state, str):
            self.change_grid(state)
        elif isinstance(state, list):
            self.load_records(state)
        return self

    def set_state(self, state: int):
        self.state_pos = state >> self.size
        self.state_statu = state ^ (self.state_pos << self.size)
        return self

    def change_grid(self, s: str):
        self.set_state(0)
        for i, v in enumerate(s.split("|")):
            self.put_chess(int(v), (i % 2) + 1)

    def s(self, v):
        return ["-", "O", "X"][v]

    def to_str(self, score: dict):
        ret = [[f"{i}"] + [" "] * self.width for i in range(self.size // self.width)]
        for i, v in enumerate(self.grid):
            y, x = i // self.height, i % self.width
            s = self.s(v)
            if i in score:
                s = str(score[i])
            ret[y][x + 1] = s
        ret.append([" "] + [str(v) for v in range(self.width)])
        return [" ".join(row) for row in ret]

    def load_records(self, records):
        self.set_state(0)
        for i, idx in enumerate(records):
            self.put_chess(idx, (i % 2) + self.STATE_FIRST)
        return self
