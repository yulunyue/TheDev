from enum import IntEnum

S = "○●"

DR = [[0, 1], [1, 0], [1, 1], [-1, 1]]


class StateEnum(IntEnum):
    STATE_NULL = 0
    STATE_40 = 1
    STATE_13 = 2


class Constant:
    HEIGHT = 7
    WIDTH = 9
    TRUN_INDEX = 0

    def __init__(self) -> None:
        self.init_score()
        self.init_w()
        self.init_lines()

    def init_score(self):
        key2 = {(4, 0): [StateEnum.STATE_40, 0.1], (1, 3): [StateEnum.STATE_13, 0.09]}
        self.scores = [[None] * (1 << 8), [None] * (1 << 8)]
        for i in range(1 << 8):
            ct = [0] * 4
            s = i
            while s > 0:
                ct[s & 3] += 1
                s = s >> 2
            if ct[3]:
                continue
            self.scores[0][i] = key2.get((ct[1], ct[2]), [StateEnum.STATE_NULL, 0])
            self.scores[1][i] = key2.get((ct[2], ct[1]), [StateEnum.STATE_NULL, 0])

        # logger.info([bin(self.WINSCORE[0]),bin(self.WINSCORE[1])])

    def init_w(self):
        self.COLS = [4, 3, 5, 2, 6, 1, 7, 0, 8]
        self.MASK_FULL_HEIGHT = (1 << self.HEIGHT + 1) - 1
        self.MASK_FULL = (1 << ((self.HEIGHT + 1) * self.WIDTH)) - 1
        self.state_pos = []
        self.INIT_MASK = 0
        self.HEIGHT_MASK0 = []
        self.HEIGHT_MASK1 = []
        self.HEIGHT_POS_MASK = []
        for i in range(4):
            self.state_pos.append([1 << (i * 2), 1 << (i * 2 + 1)])

        for col in range(self.WIDTH):
            pos = col * (self.HEIGHT + 1)
            pos_state = 1 << pos
            self.INIT_MASK |= 1 << pos
            self.HEIGHT_POS_MASK.append(
                [pos_state << (self.HEIGHT + 1), pos_state, self.MASK_FULL - pos_state]
            )
            # logger.info([col,bin(pos_state<<self.HEIGHT)])
            self.HEIGHT_MASK1.append(self.MASK_FULL_HEIGHT << pos)
            self.HEIGHT_MASK0.append(self.MASK_FULL - self.HEIGHT_MASK1[-1])

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

    def lines_to_mask(self, lines):
        pos_map = dict()
        msgs = dict()
        pt = [["?"] * self.WIDTH for _ in range(self.HEIGHT)]

        def set_pos(y, x, v):
            k = (y, x)
            pt[y][x] = ("-" + S)[v] + " "
            if k in pos_map:
                if pos_map[k][0] != v:
                    msgs[y, x, v, str(pos_map[k])] = True
                return
            pos_map[k] = [v, y, x]

        for i, state in enumerate(lines):
            for y, x, k in self.lines[i]:
                s = (state >> (k * 2)) & 3
                if s == 3:
                    raise Exception(y, x, s)
                set_pos(y, x, s)

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

    def set_pos(self, y, x, player_id, line_state, state):
        score = 0
        done = -1
        for line_id, k_id in self.point_line_id[y][x]:
            old_state = line_state[line_id]
            # if old_state & C.state_pos[k_id][player_id]:
            #     raise Exception(C.lines[k_id])
            new_state = old_state | C.state_pos[k_id][player_id]
            # p.info += f"{line_id}:{bin(new_state)}\n"
            line_state[line_id] = new_state
            new_state_id, new_score = C.scores[player_id][new_state]
            old_state_id, old_score = C.scores[player_id][old_state]
            if old_state_id != new_state_id:
                state[player_id][old_state_id] -= 1
                state[player_id][new_state_id] += 1
                score += (new_score - old_score) * [1, -1][player_id]
            if new_state_id == StateEnum.STATE_40:
                # p.info += f"[set {self.score}]"
                done = player_id + 1
            if new_state_id == StateEnum.STATE_13 and done < 0:
                # p.info += "[set -2]"
                done = -2
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
        src = self.mask_to_line(mask)
        r = ""
        info = ""
        for i, v in enumerate(src):
            r += "O" if v == dst[i] else "X"
            if v != dst[i]:
                info += f"\n{v}\n{dst[i]}\n"
        return r + info


C = Constant()
