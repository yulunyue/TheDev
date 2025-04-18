from app.yly.algo.cg.cf4.params import SE, StateEnum, ParamCt, INROW
from typing import List
import os


DATA_PATH = "data/cf4"
inf = float("inf")
S = "○●"

DR = [[0, 1], [1, 0], [1, 1], [-1, 1]]


class Constant:

    def load(self, h, w) -> None:
        self.rows = self.HEIGHT = h
        self.columns = self.WIDTH = w
        self.inarow = INROW
        self.PLAYER_NUM = 2
        self.init_w()
        self.init_score()
        self.init_lines()
        return self

    def init_score(self):
        self.scores = []
        for i in range(1 << 8):
            ct = [0] * 4
            s = i
            j = 0
            to_fill = []
            for j in range(4):
                ct[s & 3] += 1
                if s & 3 == 0:
                    to_fill.append(j)
                j += 1
                s = s >> 2
            k1 = (ct[1], ct[2])
            param = None
            if k1 in SE._params:
                param = k1
            self.scores.append([param, to_fill])
        return self

    def init_w(self):
        self.MASK_FULL_HEIGHT = (1 << self.HEIGHT + 1) - 1
        self.MASK_FULL_ALL = 0
        self.state_pos = []
        self.INIT_MASK = 0
        self.HEIGHT_POS_MASK = []
        self.POS_MASK = []
        for i in range(4):
            self.state_pos.append([1 << (i * 2), 1 << (i * 2 + 1)])
        mask0 = 0
        for col in range(self.WIDTH):
            pos = col * (self.HEIGHT + 1)
            self.MASK_FULL_ALL |= 1 << ((col + 1) * (self.HEIGHT + 1) - 1)
            self.INIT_MASK |= 1 << pos
            self.POS_MASK.append(1 << pos)
            self.HEIGHT_POS_MASK.append(mask0)
            mask0 = (mask0 << (self.HEIGHT + 1)) + self.MASK_FULL_HEIGHT
            # logger.info([col,bin(pos_state<<self.HEIGHT)])

    def init_lines(self):
        self.line_num = 0
        self.point_line_id = [
            [[[] for _ in range(len(DR))] for _ in range(self.WIDTH)]
            for _ in range(self.HEIGHT)
        ]
        self.lines = []
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                for l, (y, x) in enumerate(DR):
                    tmp = []
                    for k in range(INROW):
                        y1, x1 = i + k * y, j + k * x
                        if 0 <= y1 < self.HEIGHT and 0 <= x1 < self.WIDTH:
                            tmp.append([y1, x1, k])
                    if len(tmp) == INROW:
                        for y1, x1, idx in tmp:
                            self.point_line_id[y1][x1][l].append([self.line_num, idx])
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

    def grid_to_mask(self, grids):
        mask = 0
        for j in range(self.WIDTH):
            m = 0
            for i in range(self.HEIGHT - 1, -2, -1):
                k = i * self.WIDTH + j
                h = self.HEIGHT - i - 1
                if h == self.HEIGHT or grids[k] == 0:
                    m |= C.POS_MASK[j] << h
                    break
                if grids[k] == 2:
                    m |= C.POS_MASK[j] << h
            mask |= m
        return mask


C = Constant()
