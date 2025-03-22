from enum import IntEnum

S = "○●"

DR = [[0, 1], [1, 0], [1, 1], [-1, 1]]


class StateEnum(IntEnum):
    STATE_NULL = 0
    STATE_01 = 1
    STATE_02 = 20
    STATE_03 = 400
    STATE_04 = 8000


class Constant:
    HEIGHT = 7
    WIDTH = 9
    TRUN_INDEX = 0

    def __init__(self) -> None:
        self.init_score()
        self.init_w()
        self.init_lines()

    def init_score(self):
        key2 = {
            (0, 1): StateEnum.STATE_01,
            (0, 2): StateEnum.STATE_02,
            (0, 3): StateEnum.STATE_03,
            (0, 4): StateEnum.STATE_04,
        }
        self.scores = [[None] * (1 << 8), [None] * (1 << 8)]
        for i in range(1 << 8):
            ct = [0] * 4
            s = i
            j = 0
            to_fill = []
            while s > 0:
                ct[s & 3] += 1
                if s & 3 == 0:
                    to_fill.append(j)
                j += 1
                s = s >> 2
            if ct[3]:
                continue
            self.scores[1][i] = [
                key2.get((ct[1], ct[2]), StateEnum.STATE_NULL),
                to_fill,
            ]
            self.scores[0][i] = [
                key2.get((ct[2], ct[1]), StateEnum.STATE_NULL),
                to_fill,
            ]

        # logger.info([bin(self.WINSCORE[0]),bin(self.WINSCORE[1])])
        print(self.scores)
    def init_w(self):
        self.COLS = [4, 3, 5, 2, 6, 1, 7, 0, 8]
        self.MASK_FULL_HEIGHT = (1 << self.HEIGHT + 1) - 1
        self.MASK_FULL = (1 << ((self.HEIGHT + 1) * self.WIDTH)) - 1
        self.state_pos = []
        self.INIT_MASK = 0
        self.HEIGHT_POS_MASK = []
        for i in range(4):
            self.state_pos.append([1 << (i * 2), 1 << (i * 2 + 1)])
        mask0 = 0
        for col in range(self.WIDTH):
            pos = col * (self.HEIGHT + 1)

            self.INIT_MASK |= 1 << pos
            self.HEIGHT_POS_MASK.append(mask0)
            mask0 = (mask0 << (self.HEIGHT + 1)) + self.MASK_FULL_HEIGHT
            # logger.info([col,bin(pos_state<<self.HEIGHT)])

    def init_lines(self):
        self.line_num = 0
        self.point_line_id = [
            [[] for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)
        ]
        self.lines = []
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                for y, x in DR:
                    tmp = []
                    for k in range(4):
                        y1, x1 = i + k * y, j + k * x
                        if 0 <= y1 < self.HEIGHT and 0 <= x1 < self.WIDTH:
                            tmp.append([y1, x1, k])
                    if len(tmp) == 4:
                        for y1, x1, idx in tmp:
                            self.point_line_id[y1][x1].append([self.line_num, idx])
                        self.lines.append(tmp)
                        self.line_num += 1

    def mask_to_grid(self, mask, fn):
        for j in range(self.WIDTH):
            pos = j * (C.HEIGHT + 1)
            h_mask: int = (mask >> pos) & self.MASK_FULL_HEIGHT
            l = h_mask.bit_length() - 1
            for i in range(l):

                if h_mask & (1 << i):
                    fn(i, j, 1)
                else:
                    fn(i, j, 0)

    def set_pos(self, y, x, player_id, line_state, state, pos):
        score = 0
        done = -1
        for line_id, k_id in self.point_line_id[y][x]:
            old_state = line_state[line_id]
            # if old_state & C.state_pos[k_id][player_id]:
            #     raise Exception(C.lines[k_id])
            new_state = old_state | C.state_pos[k_id][player_id]
            # p.info += f"{line_id}:{bin(new_state)}\n"
            line_state[line_id] = new_state
            new_state_id, new_to_fill = C.scores[player_id][new_state]
            old_state_id, old_to_fill = C.scores[player_id][old_state]
            if old_state_id != new_state_id and new_state_id > 0:
                state[player_id][old_state_id] -= 1
                state[player_id][new_state_id] += 1
                score += (new_state_id - old_state_id) * [1, -1][player_id]
            if new_state_id == StateEnum.STATE_04:
                # p.info += f"[set {self.score}]"
                done = player_id + 1
            if new_state_id == StateEnum.STATE_03:
                if new_to_fill:
                    y1, x1, *args = self.lines[line_id][new_to_fill[0]]
                    pos[x1] = min(y1, pos[x1])
        # if self.score >= 1 or self.score <= -1:
        #     raise Exception(self.score)
        return score, done

    def mask_to_line(self, mask):
        line_state = [0] * self.line_num
        state = [[0] * len(StateEnum) for _ in range(2)]

        def util(i, j, v):
            self.set_pos(i, j, v, line_state, state)

        self.mask_to_grid(mask, util)
        return line_state, state

    def check_mask(self, mask, dst):
        return "O"
        src = self.mask_to_line(mask)
        r = ""
        info = ""
        for i, v in enumerate(dst):
            r += "O" if v == src[i] else "X"
            if v != src[i]:
                info += f"\n{src[i]}\n{v}\n"
        return r + info


C = Constant()
