from common.algo.base.bin_util import encode_data, decode_data, set_mask
from common.util.export import List, Dict, defaultdict, logger, log, math


def format(v):
    s = ["-", "O", "X", "#"]
    return s[v]


class BoardC5:
    STATE_NULL = 0
    STATE_FIRST = 1
    STATE_SECONED = 2
    DR = [[0, 1], [1, 0], [1, 1], [1, -1]]  # y,x 东，南，东南，西南

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
        self.points_lines = [[] for _ in range(self.size)]
        self.line_mask = []
        self.line_state = []
        self.line_center = []
        in_row = self.in_row - 1
        max_state = 1 << (2 * self.in_row)
        self.line_state_ct = defaultdict(int)
        for i in range(self.size):
            for k, (dy, dx) in enumerate(self.DR):
                iy, ix = self.get_yx(i)
                idxs = []
                mask = 0
                line_state = 0
                for j in range(-in_row, in_row + 1):
                    if j == 0:
                        continue
                    ny, nx = iy + dy * j, ix + dx * j
                    pos = (j + in_row) if j < 0 else (j + in_row - 1)
                    if 0 <= ny < self.height and 0 <= nx < self.width:
                        idx = self.yx_to_idx(ny, nx)
                        idxs.append([idx, pos])
                        mask |= self.mask_sets[idx]
                    else:
                        line_state |= 3 << (pos * 2)

                if len(idxs) < in_row:
                    continue
                line_id = len(self.line_mask)
                for idx, j in idxs:
                    self.lines[idx].append([line_id, j])
                self.points_lines[i].append(line_id)
                self.line_center.append(i)
                self.line_mask.append(mask)
                self.line_state.append(line_state)

    def init_size(self):
        self.size = self.width * self.height
        self.in_row_state = 1 << self.in_row + 1
        self.ct = [[0] * self.in_row_state, [0] * self.in_row_state]

    def init_mask(self):
        self.mask_h = (1 << self.height) - 1
        self.mask_full = (1 << self.size) - 1
        self.mask_sets = [1 << i for i in range(self.size)]
        self.mask_clear = [self.mask_full ^ (1 << i) for i in range(self.size)]
        self.set_state(0)
        return self

    def change_idx_statu(self, idx, last_player_id, cur_player_id):
        for line_id, j in self.lines[idx]:
            last_mask = self.line_state[line_id]
            new_mask = set_mask(last_mask, j * 2, 2, cur_player_id)
            self.line_mask_change(last_mask, new_mask)
            self.line_state[line_id] = new_mask

    def line_mask_change(self, f, t):
        self.line_state_ct[f] -= 1
        self.line_state_ct[t] += 1

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

    def mask_format(self, i):
        v, center_pos = self.line_mask[i], self.line_center[i]
        ret = [["0"] * self.width for _ in range(self.height)]
        center_y, center_x = self.get_yx(center_pos)
        ret[center_y][center_x] = "C"
        while v:
            low_bit = v & -v
            idx = round(math.log(low_bit, 2))
            y, x = self.get_yx(idx)
            ret[y][x] = "1"
            v ^= low_bit
        return "\n".join(["".join(row) for row in ret])

    def mask_formats(self, v):
        return [self.mask_format(u) for u in v]

    def foramt_line_state(self, v):
        in_row = self.in_row - 1
        ret = ["#"] * (in_row * 2 + 1)
        for i in range(-in_row, in_row + 1):
            if i == 0:
                ret[i + in_row] = "?"
            else:
                ret[i + in_row] = format(v & 3)
                v = v >> 2

        return "".join(ret)

    def states_all_format(self):
        return {
            self.foramt_line_state(i): v
            for i, v in enumerate(self.line_state_ct)
            if v > 0
        }

    def show(self, state=None):
        if state is None:
            state = self.get_state()
        return (
            BoardC5()
            .load(self.width, self.height, self.in_row)
            .set_state(state)
            .to_str()
        )
