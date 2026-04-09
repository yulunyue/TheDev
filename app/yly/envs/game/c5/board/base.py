from common.algo.base.bin_util import encode_data, decode_data, set_mask
from common.util.export import List, Dict, defaultdict, logger, log, math


def format(v):
    if v < 0 or v > 2:
        return "-"
    return ["-", "O", "X"][v]


class BoardC5:
    STATE_NULL = 0
    STATE_FIRST = 1
    STATE_SECONED = 2
    DR = [[0, 1], [1, 0], [1, 1], [1, -1]]  # y,x

    def load(self, width, height, in_row):
        self.width, self.height, self.in_row = width, height, in_row
        self.size = self.width * self.height
        self.init_size()
        self.init_mask()
        self.init_line_mask()
        return self

    def get_yx(self, idx):
        return idx % self.height, idx // self.height

    def yx_to_idx(self, y, x):
        return x * self.height + y

    def init_line_mask(self):
        self.lines = [[] for _ in range(self.size)]
        self.line_mask = []
        self.line_state = []
        for i in range(self.size):
            iy, ix = self.get_yx(i)
            for dy, dx in self.DR:
                idxs = [i]
                mask = self.mask_sets[i]
                for j in range(1, self.in_row):
                    ny, nx = iy + dy * j, ix + dx * j
                    if 0 <= ny < self.height and 0 <= nx < self.width:
                        idx = self.yx_to_idx(ny, nx)
                        idxs.append(idx)
                        mask |= self.mask_sets[idx]
                if len(idxs) < self.in_row:
                    continue
                for idx in idxs:
                    self.lines[idx].append(len(self.line_mask))
                self.line_mask.append(mask)
                self.line_state.append(0)

    def init_size(self):
        self.size = self.width * self.height

    def init_mask(self):
        self.mask_h = (1 << self.height) - 1
        self.mask_full = (1 << self.size) - 1
        self.mask_sets = [1 << i for i in range(self.size)]
        self.mask_clear = [self.mask_full ^ (1 << i) for i in range(self.size)]
        self.set_state(0)
        return self

    def change_idx_statu(self, idx, last_player_id, cur_player_id):
        for line_id in self.lines[idx]:
            pass

    def put_chess(self, idx, player_id):
        has_chess = self.state_pos & self.mask_sets[idx]
        last_player_id = 1 if self.state_statu & self.mask_sets[idx] else 2
        if player_id == 0:
            if has_chess:
                self.change_idx_statu(idx, last_player_id, player_id)
                self.state_pos &= self.mask_clear[idx]
            self.state_statu &= self.mask_clear[idx]
            return self
        if not has_chess:
            last_player_id = 0
        if player_id == last_player_id:
            return self
        self.change_idx_statu(idx, last_player_id, player_id)
        if player_id == 1:
            self.state_statu |= self.mask_sets[idx]
        else:
            self.state_statu &= self.mask_clear[idx]
        self.state_pos |= self.mask_sets[idx]
        return self

    def set_state_any(self, state):
        if isinstance(state, int):
            self.set_state(state)
        elif isinstance(state, str):
            self.change_grid(state)
        elif isinstance(state, list):
            self.load_records(state)
        return self

    def set_state(self, state: int):
        self.state_pos: int = state >> self.size
        self.state_statu: int = state ^ (self.state_pos << self.size)
        return self

    def get_state(self):
        return (self.state_pos << self.size) | self.state_statu

    def change_grid(self, s: str):
        self.set_state(0)
        for i, v in enumerate(s.split("|")):
            self.put_chess(int(v), (i % 2) + 1)

    def to_str(self):
        ret = [[f"{i}"] + ["-"] * self.width for i in range(self.height)]
        v = self.state_pos
        while v:
            low_bit = v & -v
            idx = round(math.log(low_bit, 2))
            y, x = self.get_yx(idx)
            player_id = 1 if self.state_statu & low_bit else 2
            ret[y][x + 1] = format(player_id)
            v ^= low_bit

        ret.append([" "] + [str(v) for v in range(self.width)])
        return "\n".join([""] + [" ".join(row) for row in ret] + [""])

    def load_records(self, records):
        self.set_state(0)
        for i, idx in enumerate(records):
            self.put_chess(idx, (i % 2) + self.STATE_FIRST)
        return self

    def get_next_states(self):
        can_move = self.mask_full ^ self.state_pos
        state = self.get_state()
        cur_player_id = self.state_pos.bit_count()
        ret = []
        while can_move:
            low_bit = can_move & -can_move
            next_state = state | (low_bit << self.size)
            if cur_player_id % 2 == 0:
                next_state |= low_bit
            ret.append(next_state)
            can_move ^= low_bit
        return ret

    def mask_format(self, v):

        ret = [["0"] * self.width for _ in range(self.height)]
        while v:
            low_bit = v & -v
            idx = round(math.log(low_bit, 2))
            y, x = self.get_yx(idx)
            ret[y][x] = "1"
            v ^= low_bit
        return "\n".join(["".join(row) for row in ret])
