from common.algo.search.param import Params, Param
from typing import List

DATA_PATH = "data/cf4"
inf = float("inf")
S = "○●"

DR = [[0, 1], [1, 0], [1, 1], [-1, 1]]


class ParamCt(Param):
    pass


class StateEnum(Params):
    def __init__(self):
        self.STATE_01 = ParamCt((0, 1)).load_value(1, 3)
        self.STATE_02 = ParamCt((0, 2)).load_value(10, 100)
        self.STATE_03 = ParamCt((0, 3)).load_value(200, 600)
        self.STATE_04 = ParamCt((0, 4)).load_value(800, 8000)
        super().__init__()


SE = StateEnum()
SE.init_param()


class Constant:

    TRUN_INDEX = 0

    def __init__(self, HEIGHT=7, WIDTH=9) -> None:
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.init_w()
        self.init_score()
        self.init_lines()

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
            k = (min(ct[1], ct[2]), max(ct[1], ct[2]))
            param = k if k in SE._params else None
            self.scores.append([param, to_fill])
        return self

    def init_w(self):
        self.COLS = [4, 3, 5, 2, 6, 1, 7, 0, 8]
        self.MASK_FULL_HEIGHT = (1 << self.HEIGHT + 1) - 1
        self.MASK_FULL_ALL = 0
        self.state_pos = []
        self.INIT_MASK = 0
        self.HEIGHT_POS_MASK = []
        for i in range(4):
            self.state_pos.append([1 << (i * 2), 1 << (i * 2 + 1)])
        mask0 = 0
        for col in range(self.WIDTH):
            pos = col * (self.HEIGHT + 1)
            self.MASK_FULL_ALL |= 1 << ((col + 1) * (self.HEIGHT + 1) - 1)
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

    def set_pos(self, y, x, player_id, line_state, end_pos):
        score = {k: 0 for k in SE._params}
        done = -1

        for line_id, k_id in self.point_line_id[y][x]:
            old_state: int = line_state[line_id]
            # if old_state & C.state_pos[k_id][player_id]:
            #     raise Exception(C.lines[k_id])
            new_state: int = old_state | C.state_pos[k_id][player_id]
            # p.info += f"{line_id}:{bin(new_state)}\n"
            line_state[line_id] = new_state
            new_line_state, null_pos = C.scores[new_state]
            old_line_state, _ = C.scores[old_state]
            if new_line_state is not None:
                score[new_line_state] += 1
            if old_line_state is not None:
                score[old_line_state] -= 1
            if new_line_state == (0, 4):
                # p.info += f"[set {self.score}]"
                done = player_id + 1
            elif new_line_state == (0, 3):
                y1, x1, _ = self.lines[line_id][null_pos[0]]
                end_pos[y1, x1] = end_pos.get((y1, x1), 0) | (1 << (1 - player_id))

        # if self.score >= 1 or self.score <= -1:
        #     raise Exception(self.score)
        return score, done

    def mask_to_line(self, mask, line_state, state, end_pos):
        done = -1
        depth = 0

        def util(i, j, v):
            nonlocal done, depth
            pos_state, done = self.set_pos(i, j, 1 - v, line_state, end_pos)
            end_pos[j] = i + 1
            for key, v in pos_state.items():
                state[key] += v
            depth += 1

        self.mask_to_grid(mask, util)
        return done, depth


C = Constant()
