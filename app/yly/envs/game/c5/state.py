from common.algo.export import AbState, Action, List
from .constant import C


class C5ACtion(Action):
    def __init__(self, src, action, dst=None, obs=None):
        super().__init__(src, action, dst)
        self.obs: dict = obs

    def show(self):
        y, x = self.action // C.width, self.action % C.width
        return f"src:{self.src.state}, dst:{self.dst.state}, action:{y},{x}, obs:{self.obs}"

    def is_self_win(self):
        win_in = C.in_row if self.src.player_id == 0 else -C.in_row
        return self.obs.get(win_in, 0) > 0

    def is_op_win(self):
        op_state = C.op_win_state if self.src.player_id == 0 else -C.op_win_state
        return self.obs.get(op_state, 0) > 0

    def get_src_reward(self, actions: List[Action]):
        pass


class State(AbState):
    @classmethod
    def new(cls, state=None, **kw) -> "State":
        if state is None:
            state = C.state
        return super().new(state, **kw)

    def get_action(self, pos):
        C.set_mask(self.state)
        obs, state = C.get_next_state(pos, self.player_id + 1)
        dst = State.new(state).set_player_id(1 - self.player_id)
        a = C5ACtion(self, pos, dst, obs=obs)
        return a

    def make_actions(self):
        actions = []
        actions_op_win = []
        can_moves = list(C.pos_status[C.STATE_NULL])
        for pos in can_moves:
            a = self.get_action(pos)
            if a.is_self_win():
                a.dst.set_done(
                    AbState.FIRST_WIN if self.player_id == 0 else AbState.SECONEND_WIN
                )
                return [a]
            if len(can_moves) == 1:
                a.dst.set_done(AbState.NO_WIN)
                return [a]
            if a.is_op_win():
                actions_op_win.append(a)
                continue
            actions.append(a)
        if not actions and not actions_op_win:
            raise Exception(self.show())
        return actions_op_win if actions_op_win else actions

    def to_str(self):
        C.set_mask(self.state)
        ret = [[f"{i}"] + [" "] * C.width for i in range(C.height)]
        for i, v in enumerate(C.grid):
            y, x = i // C.width, i % C.width
            ret[y][x + 1] = [" ", "O", "X"][v]
        ret.append([" "] + [str(v) for v in range(C.width)])
        return [" ".join(row) for row in ret]
