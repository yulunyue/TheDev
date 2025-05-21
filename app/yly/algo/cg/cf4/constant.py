from app.yly.algo.cg.cf4.params import SE, StateEnum, ParamCt, INROW
from common.algo.manage import get_log
from typing import List
import math
import os

logger = get_log("cf4", mode="a+")

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
            self.scores.append([ct[1], ct[2], to_fill])
        return self

    def line_fmt(self, v):
        s2 = ""
        for j in range(4):
            s2 += ("?" + S)[v & 3]
            v = v >> 2
        return s2

    def init_w(self):
        self.WIDTH_POINTS = [0] * self.WIDTH
        w = (self.WIDTH - 1) // 2
        for i in range(self.WIDTH):
            self.WIDTH_POINTS[i] = -abs(i - w)

    def init_w2(self):
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
        n = self.WIDTH * self.HEIGHT
        self.point_line_id = [[] for _ in range(n)]
        self.lines = []
        for ii in range(n):
            i, j = ii // self.WIDTH, ii % self.WIDTH
            for l, (y, x) in enumerate(DR):
                tmp = []
                for k in range(INROW):
                    y1, x1 = i + k * y, j + k * x
                    if 0 <= y1 < self.HEIGHT and 0 <= x1 < self.WIDTH:
                        tmp.append([y1, x1, k, len(self.lines)])
                if len(tmp) != INROW:
                    continue
                for y1, x1, idx, line_id in tmp:
                    # if y1 == 1 and x1 == 0 and idx != 0:
                    #     continue
                    jj = y1 * self.WIDTH + x1
                    self.point_line_id[jj].append([line_id, l, idx])
                self.lines.append(tmp)

    def mask_to_grid(self, mask):
        ret = [0] * (self.HEIGHT * self.WIDTH)
        mask_full = (1 << self.HEIGHT + 1) - 1
        for j in range(self.WIDTH):
            pos = j * (C.HEIGHT + 1)
            h_mask: int = (mask >> pos) & mask_full
            h = h_mask.bit_length() - 2
            while h >= 0:
                k = (C.HEIGHT - h - 1) * self.WIDTH + j
                if h_mask & (1 << h):
                    ret[k] = 2
                else:
                    ret[k] = 1
                h -= 1
        return ret

    def get_grid_sequence(self, grid):
        pos = []
        zero_num = 0
        col = [0] * C.WIDTH
        for i in range(self.WIDTH):
            while col[i] < C.HEIGHT:
                k = col[i] * self.WIDTH + i
                if grid[k] != 0:
                    break
                col[i] += 1
                zero_num += 1
        player_id = (C.WIDTH * C.HEIGHT - zero_num + 1) % 2 + 1
        while True:
            j = None
            for i in range(self.WIDTH):
                if col[i] == self.HEIGHT:
                    continue
                k = col[i] * self.WIDTH + i
                if grid[k] == player_id:
                    j = i
                    k1 = (1 + col[i]) * self.WIDTH + i
                    if k1 < len(grid) and grid[k1] == 3 - player_id:
                        break
            if j is None:
                break
            pos.append(str(j + 1))
            player_id = 3 - player_id
            col[j] += 1
        pos.reverse()
        return "".join(pos)

    def sequence_to_grid(self, seq):
        col = [self.HEIGHT - 1] * self.WIDTH
        player_id = 1
        grid = [0] * self.WIDTH * self.HEIGHT
        for k in seq:
            k = int(k) - 1
            i = col[k] * self.WIDTH + k
            grid[i] = player_id
            player_id = 3 - player_id
            col[k] -= 1
        return grid

    def get_api_score(self, pos):

        move_length = len(pos)
        from common.service.api import Api

        score = (
            Api()
            .set_cache()
            .get(
                f"https://connect4.gamesolver.org/solve?pos={pos}",
            )["score"]
        )
        best = -100
        for s in score:
            if s == 100:
                continue
            best = max(best, s)
        v = 0
        if best > 0:
            v = math.floor((45 - move_length) / 2) - best
            return 1, v * 2
        elif best < 0:
            v = math.floor((44 - move_length) / 2) + best
            return -1, v * 2 + 1
        return 0, 0

    def grid_view(self, grid):
        h, w = C.HEIGHT, C.WIDTH
        ret = []
        col = [-1] * C.WIDTH
        for i in range(h):
            tmp = [f"{i} "]
            for j in range(w):
                v = grid[i * w + j]
                if isinstance(v, int) and 1 <= v <= 2:
                    tmp.append(f"{S[v-1]} ")
                else:
                    col[j] = max(col[j], i)
                    tmp.append("- ")
            ret.append("".join(tmp))
        ret.append("  " + " ".join([str(i) for i in range(w)]))
        pos = self.get_grid_sequence(grid)
        ret.append(f"P: {pos}")
        max_score = -1
        INFO = ["NOWIN", "WIN", "LOSE"]
        for j, v in enumerate(col):
            if v == -1:
                continue
            score, step = self.get_api_score(pos + str(j + 1))
            score = -score
            if score != 0:
                ret.append(f"U: {S[len(pos)%2]} {INFO[score]}, a:{j}, s:{step}")
            if score > max_score:
                max_score = score
        ret.append(f"R: {S[len(pos)%2]} {INFO[max_score]}")
        # a = self.sequence_to_grid(pos)
        # logger.info([f"xx{a==grid}", a, grid])
        return "\n".join(ret)

    def grid_to_mask(self, grids):
        mask = 0
        for j in range(self.WIDTH):
            i = self.HEIGHT - 1
            while i >= 0:
                s = grids[i * self.WIDTH + j]
                pos = C.HEIGHT - i - 1 + j * (self.HEIGHT + 1)
                if s == 0:
                    mask |= 1 << pos
                    break
                if s == 2:
                    mask |= 1 << pos
                i -= 1
                if i == -1:
                    pos = C.HEIGHT + j * (self.HEIGHT + 1)
                    mask |= 1 << pos
        return mask

    def grid_to_line_state(self, grid):
        line_state, row_idx = (
            [0] * len(C.lines),
            [-1] * C.WIDTH,
        )
        player_id = 0
        for i in range(self.HEIGHT * self.WIDTH):
            y, x = i // self.WIDTH, i % self.WIDTH
            if grid[i] == 0:
                row_idx[x] = max(row_idx[x], y)
            else:
                for line_id, l, idx in self.point_line_id[i]:
                    line_state[line_id] |= grid[i] << (idx * 2)
                player_id = 1 - player_id
        return (
            row_idx,
            set(x for x in range(self.WIDTH) if row_idx[x] != C.HEIGHT),
            line_state,
            player_id,
        )

    def mask_to_line_state(self, mask):
        return self.grid_to_line_state(self.mask_to_grid(mask))


C = Constant()
