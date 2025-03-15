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
            self.state_pos.append(
                [1 << (i * 2), 1 << (i * 2 + 1), (1 << 8) - 1 - (3 << (i * 2))]
            )

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

    def check_mask(self, mask_dst, lines):
        masks = 0
        for i, state in enumerate(lines):
            for y1, x1, k in self.lines[i]:
                s = (state >> (k * 2)) & 3


C = Constant()
