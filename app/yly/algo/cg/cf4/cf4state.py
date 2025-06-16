from app.yly.algo.cg.cf4.constant import C, DR, S
from common.algo.search.state import State
from typing import Dict


class F4State(State):
    STATE_STORE: Dict[int, "F4State"] = dict()

    def __init__(self, state):
        super().__init__(state, player_id=0, depth=0)

    @classmethod
    def new_state(cls, state, x=None):
        if isinstance(state, F4State):
            mask = C.pust_to_mask(state.state, x, state.player_id)
        else:
            mask = state
        if mask not in F4State.STATE_STORE:
            F4State.STATE_STORE[mask] = F4State(mask)
            if isinstance(state, F4State):
                F4State.STATE_STORE[mask].load_from_parent(state, x)
            else:
                F4State.STATE_STORE[mask].load_from_mask(mask)
        return F4State.STATE_STORE[mask]

    @classmethod
    def get_init_state(cls):
        return cls.new_state(C.grid_to_mask([0] * (C.WIDTH * C.HEIGHT)))

    def to_str(self):
        return C.grid_view(self.state)

    def load_from_mask(self, mask):
        (
            self.row_idx,
            self.can_move,
            self.line_state,
            self.player_id,
            self.depth,
            self.ct,
        ) = C.mask_to_line_state(mask)

    def load_from_grid(self, grid):
        self.row_idx, self.can_move, self.line_state, self.player_id, self.depth = (
            C.grid_to_line_state(self.state)
        )

    def load_from_parent(self, p: "F4State", x: int):
        self.depth += p.depth + 1
        self.player_id = 1 - p.player_id
        # self.grid = p.grid.copy()
        self.row_idx = p.row_idx.copy()
        self.ct = p.ct.copy()
        self.line_state = p.line_state.copy()
        self.can_move = p.can_move.copy()
        k = self.row_idx[x] * C.WIDTH + x
        for line_id, l, idx, *args in C.point_line_id[k]:
            old_state = self.line_state[line_id]
            self.line_state[line_id] |= [1, 2][p.player_id] << (2 * idx)
            ct1, ct2, _ = C.scores[self.line_state[line_id]]
            if ct1 == C.inarow:  # 先手胜
                self.done = -1
            elif ct2 == C.inarow:  # 后手胜利
                self.done = 1
            C.state_change(self.ct, old_state, self.line_state[line_id], self.player_id)

        self.row_idx[x] -= 1
        if self.row_idx[x] == -1:
            self.can_move.remove(x)
        if len(self.can_move) == 0 and self.done is None:
            self.done = 0

    def get_action(self, x):
        from app.yly.algo.cg.cf4.cf4action import F4Action

        return F4Action(self, self.row_idx[x], x, F4State.new_state(self, x))

    def get_actions_all(self):
        return self.can_move

    _info = ""

    def get_info(self):
        return self._info

    def get_reward(self, **kw):
        return self.get_max_action_reward()
