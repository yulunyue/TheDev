from common.algo.export import AbState, Action
from .constant import C


class State(AbState):
    @classmethod
    def new(cls, state=None, **kw):
        if state is None:
            state = C.state
        return super().new(state, **kw)

    def make_actions(self):
        C.set_mask(self.state)
        actions = []
        actions_op_win = []
        can_moves = list(C.pos_status[C.STATE_NULL])
        for pos in can_moves:
            obs, state = C.get_next_state(pos, self.player_id + 1)
            dst = State.new(state)
            a = Action(self, pos, dst).set_data(obs=obs)
            if obs.get(C.in_row, 0) > 0:
                dst.set_done(2)
                return [a]
            elif obs.get(-C.in_row, 0) > 0:
                dst.set_done(1)
                return [a]
            if (self.player_id == 0 and obs.get(C.in_row - 1, 0) > 0) or (
                self.player_id == 1 and obs.get(1 - C.in_row, 0) > 0
            ):
                actions_op_win.append(a)
                continue
            actions.append(a)
        if not actions and not actions_op_win:
            raise Exception(self.state)
        return actions_op_win if actions_op_win else actions

    def to_str(self):
        C.set_mask(self.state)
        ret = [[" "] * C.width for _ in range(C.height)]
        for i, v in enumerate(C.grid):
            y, x = i // C.width, i % C.width
            ret[y][x] = str(v)
        return [" ".join(row) for row in ret]
