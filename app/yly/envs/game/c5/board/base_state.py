from .base import BoardC5, set_mask


class BoardC5State(BoardC5):
    def init_mask_state(self):
        self.max_state = (1 << (2 * (self.in_row * 2 - 1))) - 1
        self.mask_state = [0] * self.max_state
        self.line_ct = {}
        for mk in range(self.max_state):
            if mk & (mk - 1):  # 有11
                continue
            t1 = mk & 3
            ct = 1
            mask = mk >> 2
            alive = t1 == 0
            while mask:
                t2 = mask & 3
                if t1 != t2:
                    if t1 != 0:
                        if t2 == 0:
                            pass
                    ct = 0
                t1 = t2
                ct += 1
                mask = mask >> 2

    def in_row2(self):
        return self.in_row

    def init_lines(self):
        self.lines = [[] for _ in range(self.size)]
        self.line_pos = []
        self.line_state = []
        in_row2 = self.in_row2()
        for i in range(self.size):
            l1, l2 = self.get_l(i)
            for dy, dx in self.DR:
                poss = []
                for k in range(-in_row2 + 1, in_row2):
                    idx = self.get_dis(l1, l2, dy, dx, k)
                    if idx is None:
                        continue
                    poss.append([idx, k])
                if len(poss) < in_row2:
                    continue
                line_id = len(self.line_state)
                self.line_pos.append(poss)
                for j, k in poss:
                    self.lines[j].append([line_id, k])
                self.line_state.append(0)

    def get_line_ct(self):
        return {k: v for k, v in self.line_ct.items() if v > 0}

    def load(self, width=6, height=6, in_row=4):
        super().load(width, height, in_row)
        self.init_mask_state()
        self.init_lines()
        return self

    def change_chess_statu(self, idx, player_id):
        self.change_line_statu(idx, player_id)
        return super().change_chess_statu(idx, player_id)

    def change_line_statu(self, idx, player_id):
        for lid, pos in self.lines[idx]:
            old_state = self.line_state[lid]
            self.line_state[lid] = set_mask(
                self.line_state[lid], pos * self.CHESS_SIZE, self.CHESS_SIZE, player_id
            )
            s1, s2 = self.mask_state[old_state], self.mask_state[self.line_state[lid]]
            self.line_ct[s1] -= 1
            self.line_ct[s2] += 1
        # logger.map(idx=idx, cid=self.grid[idx], newid=player_id)

        # ps = [[[v[0] // self.width, v[0] % self.width] for v in self.line_pos[lid]]]
        # if abs(s1) == self.in_row + 1:
        #     log.debug(f"LOS pos={ps} o:{s1} n:{self.line_ct[s1]}")
        # if abs(s2) == self.in_row + 1:
        #     log.debug(f"NEW pos={ps} o:{s2} n:{self.line_ct[s2]}")

    def get_win_pos(self, state):
        for i, s in enumerate(self.line_state):
            if self.mask_state[s] == state:
                return [d[0] for d in self.line_pos[i] if self.grid[d[0]] == 0][0]
