from common.util.export import get_log
from typing import List
import math
import os

logger = get_log("cf4")

DATA_PATH = "data/cf4"
inf = float("inf")
S = "○●"

DR = [[0, 1], [1, 0], [1, 1], [-1, 1]]
CHEN = [10 ** (6 - i) for i in range(7)]
INROW = 4


class Constant:

    def load(self, h, w) -> None:
        self.rows = self.HEIGHT = h
        self.columns = self.WIDTH = w
        self.mid = (self.WIDTH - 1) / 2
        self.inarow = INROW
        self.PLAYER_NUM = 2

        self.init_w2()
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

    # def init_w(self):
    #     self.WIDTH_POINTS = [0] * self.WIDTH
    #     w = (self.WIDTH - 1) // 2
    #     for i in range(self.WIDTH):
    #         self.WIDTH_POINTS[i] = -abs(i - w)

    def init_w2(self):
        self.MASK_FULL_HEIGHT = (1 << self.HEIGHT + 1) - 1
        self.MASK_FULL_ALL = 0
        self.state_pos = []
        self.INIT_MASK = 0
        self.HEIGHT_POS_MASK = []
        # self.POS_MASK = []
        for i in range(4):
            self.state_pos.append([1 << (i * 2), 1 << (i * 2 + 1)])
        mask0 = 0
        for col in range(self.WIDTH):
            pos = col * (self.HEIGHT + 1)
            self.MASK_FULL_ALL |= 1 << ((col + 1) * (self.HEIGHT + 1) - 1)
            self.INIT_MASK |= 1 << pos
            # self.POS_MASK.append(1 << pos)
            mask0 = (mask0 << (self.HEIGHT + 1)) + self.MASK_FULL_HEIGHT
            self.HEIGHT_POS_MASK.append(mask0)
            # logger.info([col,bin(pos_state<<self.HEIGHT)])

    def mask_to_row(self, mask, col):
        a: int = mask & self.HEIGHT_POS_MASK[col]
        return (a.bit_length() - 1) % (self.HEIGHT + 1)

    def pust_to_mask(self, mask, col, player_id):
        pos = col * (self.HEIGHT + 1) + self.mask_to_row(mask, col)
        m = 1 << pos
        mask |= m << 1
        if player_id == 0:
            mask &= ~m
        else:
            mask |= m
        return mask

    def init_lines(self):
        n = self.WIDTH * self.HEIGHT
        self.point_line_id = [[] for _ in range(n)]
        line_map = dict()
        self.lines = []
        for ii in range(n):
            i, j = ii // self.WIDTH, ii % self.WIDTH
            for l, (y, x) in enumerate(DR):
                tmp = []
                for k in range(INROW):
                    y1, x1 = i + k * y, j + k * x
                    if 0 <= y1 < self.HEIGHT and 0 <= x1 < self.WIDTH:
                        tmp.append([y1, x1, k])
                if len(tmp) != INROW:
                    continue
                key = tmp[0][0], tmp[0][1], tmp[-1][0], tmp[-1][1]
                if key in line_map:
                    continue
                line_map[key] = tmp
                for line_id, (y1, x1, idx) in enumerate(tmp):
                    # if y1 == 1 and x1 == 0 and idx != 0:
                    #     continue
                    jj = y1 * self.WIDTH + x1
                    self.point_line_id[jj].append(
                        [len(self.lines), l, line_id, idx, key]
                    )
                self.lines.append(tmp)

    def init_line2(self):
        self.lines = []
        for ii in range(self.WIDTH * self.HEIGHT):
            for l, (y, x) in enumerate(DR):
                i, j = ii // self.WIDTH, ii % self.WIDTH
                k = 0
                while k < 2 * INROW:
                    y1, x1 = i + k * y, j + k * x
                    if 0 <= y1 < self.HEIGHT and 0 <= x1 < self.WIDTH:
                        break
                    k += 1

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
        if isinstance(grid, int):
            grid = self.mask_to_grid(grid)
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
        from common.service.export import Api

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

    def get_api_score_all(self, grid, col):
        ret = []
        pos = self.get_grid_sequence(grid)
        ret.append(f"P: {pos}")
        max_score = -1
        INFO = ["NOWIN", "WIN", "LOSE"]
        for j, v in enumerate(col):
            if v == -1:
                continue
            score, step = self.get_api_score(pos + str(j + 1))
            score = -score
            # if score != 0:
            ret.append(f"U{j}: {S[len(pos)%2]}:{INFO[score]}, s:{step}")
            if score > max_score:
                max_score = score
        ret.append(f"R: {S[len(pos)%2]} {INFO[max_score]}")
        return ret

    def grid_view(self, grid):
        if isinstance(grid, int):
            grid = self.mask_to_grid(grid)
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

    def state_change(self, ct, old_state, new_state, player_id):
        new_ct1, new_ct2, _ = C.scores[new_state]
        old_ct1, old_ct2, _ = C.scores[old_state]
        if new_ct1 > 1 and new_ct2 == 0:
            ct[2 * (self.inarow - new_ct1) + player_id] += 1
        if new_ct2 > 1 and new_ct1 == 0:
            ct[2 * (self.inarow - new_ct2) + 1 - player_id] += 1
        if old_ct1 > 1 and old_ct2 == 0:
            ct[2 * (self.inarow - old_ct1) + player_id] -= 1
        if old_ct2 > 1 and old_ct1 == 0:
            ct[2 * (self.inarow - old_ct2) + 1 - player_id] -= 1

    def grid_to_line_state(self, grid):
        line_state, row_idx = (
            [0] * len(C.lines),
            [-1] * C.WIDTH,
        )
        player_id = 0
        depth = 0
        ct = [0] * 6
        for i in range(self.HEIGHT * self.WIDTH):
            y, x = i // self.WIDTH, i % self.WIDTH
            if grid[i] == 0:
                row_idx[x] = max(row_idx[x], y)
            else:
                for line_id, l, idx, *args in self.point_line_id[i]:
                    line_state[line_id] |= grid[i] << (idx * 2)
                player_id = 1 - player_id
                depth += 1
        return (
            row_idx,
            set(x for x in range(self.WIDTH) if row_idx[x] != C.HEIGHT),
            line_state,
            player_id,
            depth,
            ct,
        )

    def mask_to_line_state(self, mask):
        return self.grid_to_line_state(self.mask_to_grid(mask))

    def count_line_num(self, num):
        w1, h1 = max(self.WIDTH - num + 1, 0), max(self.HEIGHT - num + 1, 0)
        ret = self.WIDTH * h1 + self.HEIGHT * w1 + 2 * w1 * h1
        # logger.info(f"xxx:{num},{ret}")
        return ret

    def count_line_all(self):
        ret = 0
        for i in range(INROW, 2 * INROW):
            ret += self.count_line_num(i)
        return ret

    def get_grid_by_line_state(self, line_state):
        ret = []
        for v in C.point_line_id:
            line_id, l, idx, *args = v[0]
            state = (line_state[line_id] >> (idx * 2)) & 3
            ret.append(state)
        return ret

    def get_c4_points(self, line_state, cy, x, player_id):
        """
        POINTS: A04,B04,-B14,-A14,xn(A03,B03),xn(A02,B02),-xn(A12,B12)
        """
        pts, ptsrc = [], []
        op = 1
        for i in range(C.HEIGHT):
            y = cy - i
            if y >= 0:
                points = self.get_action_points(line_state, y, x, player_id)
                ptsrc.extend(points)
                if i == 1:
                    pts[2:2] = [op * points[1], op * points[0]]
                    if abs(points[4]) < min(points[2], 2):
                        pts[4:4] = [op * points[2]]
                        if abs(points[5]) < min(points[3], 2):
                            pts[5:5] = [op * points[3]]
                        else:
                            pts[7:7] = [op * points[3]]
                    else:
                        pts[6:6] = [op * points[2], op * points[3]]
                    pts.extend([v * op for v in points[4:]])
                else:
                    pts.extend([v * op for v in points])
                # if i <= 1:

                #     self._info += f"point_sl{i}:{points}\n"
            else:
                pts.extend([0] * 6)
            op *= -1
        return pts, ptsrc

    def get_point_dr(self, line_state, y, x, player_id):
        i = y * self.WIDTH + x
        rt = [0] * 6
        dr_ct = [[0, 0, 0, 0], [0, 0, 0, 0]]
        for line_id, l, idx, *args in C.point_line_id[i]:
            self_ct, op_ct, _ = C.scores[line_state[line_id]]
            # logger.info([self_ct, op_ct, l, idx, args])
            if player_id == 1:
                self_ct, op_ct = op_ct, self_ct
            # self._info += f"line:{C.lines[line_id]},l:{[l,ct0,ct1]},state:{C.line_fmt(self.line_state[line_id])}\n"
            if self_ct == 0 and op_ct:
                #
                dr_ct[1][l] = max(dr_ct[1][l], op_ct)
            if op_ct == 0 and self_ct:
                dr_ct[0][l] = max(dr_ct[0][l], op_ct)
        for i, ct in enumerate(dr_ct):
            for v in ct:
                if v:
                    j = (3 - v) * 2 + i
                    rt[j] += 1
        return rt

    def calc_point_value(self, points, cha=None):
        score = 0
        if cha is None:
            cha = CHEN
        for i, v in enumerate(points):
            score += CHEN[i] * v
        return score

    def extend_first_action_scroe(self, points, x):
        xv = int(self.mid - abs(x - self.mid))
        return points + [xv]

    def get_action_points(self, line_state, y, x, player_id):
        """
        POINT0: A4,A3,A2
        POINT1: B4,B3,B2
        POINTS: A4,B4,xn(A3,B3),xn(A2,B2)
        """
        points = self.get_point_dr(line_state, y, x, player_id)
        # self._info += f"dr_ct:{dr_ct}"
        for i, j in [[2, 3], [4, 5]]:
            if points[i] < points[j]:
                points[i], points[j] = points[j], points[i]

        return points


C = Constant()
