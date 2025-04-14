from typing import Dict, List
from common.algo.search.state import State, Action, inf
from common.algo.search.mctssearch import MctsSearchTree, MctsNode
from app.yly.algo.cg.cf4.constant import C, SE, S, StateEnum
from collections import defaultdict
import json


def board_format(borad):
    mask = C.grid_to_mask(borad)
    info = ["", f"---{mask}---"]
    for i in range(C.HEIGHT):
        info.append("".join([str(v) for v in borad[i * C.WIDTH : (i + 1) * C.WIDTH]]))
    return "\n".join(info), mask


class F4State(MctsNode):
    name = "f4state"
    info = ""
    parent: "F4State"

    def __init__(self, mask, depth=0) -> None:
        self.mask = mask
        super().__init__(depth % 2, depth)

    def __str__(self):
        return self.to_str()

    def to_str(self, info=""):
        ret = [["- "] * C.WIDTH for i in range(C.HEIGHT)]
        ret.append([f"{i} " for i in range(C.WIDTH)])

        def util(i, j, v):
            ret[C.HEIGHT - i - 1][j] = S[v] + " "

        C.mask_to_grid(self.mask, util)
        for j in range(C.WIDTH):
            for i in range(self.end_pos[j], C.HEIGHT):
                if (i, j) in self.end_pos:
                    ret[C.HEIGHT - i - 1][j] = f"{self.end_pos[i,j]} "

        # check_info = C.check_mask(self.mask, [self.line_state, self.state])

        # state_info = [""]
        # for k, v in self.state.items():
        #     s, player_id = k
        #     if s == StateEnum.STATE_NULL:
        #         continue
        #     state_info.append(f"{S[player_id]}:{str(s).split('.').pop()}:{v}")
        # state_info = "\n  ".join(state_info)

        check_info = ""

        # b = Baoli()
        # bv = b.search(self, depth=20, state_max_num=4000)
        return "\n".join(
            [
                "",
                "**" * (C.WIDTH + 1),
                f"mask: {self.mask}",
            ]
            + [
                f"{C.HEIGHT-i-1 if i!=C.HEIGHT else ' '} " + "".join(v)
                for i, v in enumerate(ret)
            ]
            + [
                f"done: {self.done}; depth: {self.depth};",
                f"playerid: {self.player_id}{S[self.player_id]};",
                # f"state:{state_info}",
                # f"sear:[{bv}][{b.state_count}],{'%.3f'%b.use_time};",
                # info,
                # f"info:{self.info}; check:{check_info}",
            ]
            + ["**" * (C.WIDTH + 1), ""]
        )

    @property
    def key(self):
        return str(self.mask)

    def init_root(self, h, w):
        C.load(h, w)
        self.line_state = [0] * C.line_num
        self.state = {k: 0 for k in SE._params}
        self.end_pos = {x: 0 for x in range(C.WIDTH)}
        self.grid = [0] * (h * w)
        if self.mask is None:
            self.mask = C.INIT_MASK
        if self.mask != C.INIT_MASK:
            self.mask, self.done, self.depth = C.mask_to_line(
                self.mask, self.line_state, self.state, self.end_pos, self.grid
            )
            self.player_id = self.depth % 2
        else:
            self.depth = 0
            self.player_id = 0
        return self

    def get_action(self, col, **kw):
        x = col * (C.HEIGHT + 1)
        mask0 = self.mask >> x
        # y = (mask0 & C.MASK_FULL_HEIGHT).bit_length() - 1
        y = self.end_pos[col]
        if y == C.HEIGHT:
            return
        depth = self.depth + 1
        if depth % 2 == 0:
            mask0 |= 2 << y
        else:
            mask0 ^= 3 << y
        mask = (mask0 << x) | (self.mask & C.HEIGHT_POS_MASK[col])
        if mask not in STORE_STATE:
            STORE_STATE[mask] = F4State(mask, depth).init_state(col, y, self)
            if mask & C.MASK_FULL_ALL == C.MASK_FULL_ALL:
                STORE_STATE[mask].done = 0
        from app.yly.algo.cg.cf4.f4action import F4Action

        return F4Action().load(self, y, col, STORE_STATE[mask])

    def init_state(self, x, y, p):
        p: F4State = p
        self.end_pos = p.end_pos.copy()
        self.line_state = p.line_state.copy()
        self.state = p.state.copy()
        self.grid = p.grid.copy()
        state, self.done = C.set_pos(
            y, x, self.player_id, self.line_state, self.end_pos
        )
        for key, v in state.items():
            self.state[key] += v

        self.end_pos[x] = y + 1
        self.grid[(C.HEIGHT - self.end_pos[x]) * C.WIDTH + x] = 2 - self.player_id
        return self

    _debug_file = None

    def debug(self, info=""):
        from common.util.fp import File

        if not F4State._debug_file:
            fp = File("data/log/c4.txt").write_file("init\n")
            F4State._debug_file = open(fp.path, "a", encoding="utf-8")
        if info.startswith("msg"):
            F4State._debug_file.write(f"\n-----{info}----\n")
        else:
            F4State._debug_file.write(self.to_str(info))

    def get_actions(self, depth=1, **kw):
        if depth == 0 or self.done > 0:
            return []
        if self.actions is None:
            actions = []
            flag = True
            for col in range(C.WIDTH):
                a = self.get_action(col, **kw)
                if a is None:
                    continue
                s = self.end_pos.get((self.end_pos[col], col), 0)
                if s & self.win_done:
                    actions = [a]
                    break
                if s & self.op_done:
                    actions = [a]
                    flag = False
                if flag:
                    actions.append(a)
            self.actions = actions
            # self.actions = sorted(
            #     actions, key=lambda v: v.get_reward(SE) * [-1, 1][v.dst.player_id]
            # )
        return self.actions

    def load_from_board(self, board, rows, columns):
        pass

    @property
    def win_done(self):
        return 2 if self.player_id else 1

    @property
    def op_done(self):
        return 3 - self.win_done


STORE_STATE: Dict[int, F4State] = dict()
