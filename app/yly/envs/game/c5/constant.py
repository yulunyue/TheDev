from common.algo.export import encode_data, decode_data, set_mask
from common.util.export import List, Dict, defaultdict


class Constant:
    STATE_NULL = 0
    STATE_FIRST = 1
    STATE_SECONED = 2
    BIT_SIZE = 2
    DR = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    in_row = 4

    def __init__(self):
        self.init_mask_state()

    def init_mask_state(self):
        self.max_state = (1 << (self.BIT_SIZE * self.in_row)) - 1
        self.mask_state = [0] * self.max_state
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
                self.mask_state[mk] = ct[2]

    def load(self, width=6, height=6):
        self.width = width
        self.height = height
        self.size = self.width * self.height
        self.row_bit = self.BIT_SIZE * self.width
        self.height_bit = self.BIT_SIZE * self.height
        self.mask_cloumn = (1 << self.height_bit) - 1
        self.mask_row = (1 << self.row_bit) - 1
        self.mask_bit = (1 << self.BIT_SIZE) - 1
        self.grid = [Constant.STATE_NULL] * self.size
        self.pos_status: Dict[int, set] = {
            self.STATE_NULL: set(range(self.size)),
            self.STATE_FIRST: set(),
            self.STATE_SECONED: set(),
        }
        self.state = 0
        self.init_lines()
        return self

    def init_lines(self):
        self.lines = [[] for _ in range(self.size)]
        self.line_state = []
        for i in range(self.size):
            y, x = i // self.size, i % self.size
            for dy, dx in self.DR:
                poss = []
                for k in range(self.in_row):
                    y1, x1 = dy * k + y, dx * k + x
                    if y1 < 0 or x1 < 0 or y1 >= self.height or x1 >= self.width:
                        continue
                    poss.append([dy, dx, k])
                if len(poss) != self.in_row:
                    continue
                line_id = len(self.line_state)
                for y1, x1, k in poss:
                    j = y1 * self.width + x1
                    self.lines[j].append([line_id, k])
                self.line_state.append(0)

    def put_chess(self, idx, player_id):
        ans = defaultdict(int)
        if self.grid[idx] == player_id:
            raise Exception(idx, player_id)
        for lid, pos in self.lines[idx]:
            old_state = self.line_state[lid]
            new_state = set_mask(
                old_state, pos * self.BIT_SIZE, self.BIT_SIZE, player_id
            )
            ans[self.mask_state[old_state]] -= 1
            ans[self.mask_state[new_state]] += 1
        self.pos_status[player_id].add(idx)
        self.pos_status[self.grid[idx]].remove(idx)
        self.grid[idx] = player_id
        self.state = set_mask(self.state, idx * self.BIT_SIZE, self.BIT_SIZE, player_id)
        return ans, self.state

    def set_mask(self, state):
        if self.state == state:
            return self
        state1, state2 = self.state, state
        for y in range(self.height):
            state3, state4 = state1 & self.mask_cloumn, state2 & self.mask_cloumn
            if state3 == state4:
                continue
            for x in range(self.width):
                if state3 & self.mask_bit != state4 & self.mask_bit:
                    self.put_chess(y * self.width + x, state4 & self.mask_bit)
                state4 >> self.BIT_SIZE
                state3 >> self.BIT_SIZE
            state1 = state1 >> self.row_bit
            state2 = state2 >> self.row_bit
        return self


C = Constant().load()
