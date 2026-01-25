from .cf4action import F4Action
from .constant import C
from common.algo.search.states.state import AbState, Action
from common.util.export import List, Dict, logger, log
from .env import ENV


class C4ACtion(Action):
    def __init__(self, src, action, dst=None, obs=None):
        super().__init__(src, action, dst)
        self.obs: dict = obs

    def show(self):
        return f"src:{self.src.state}, dst:{self.dst.state}, action:{self.action}{ENV.s(self.src.player_id+1)}, obs:{self.obs}"

    def is_self_win(self):
        win_in = ENV.in_row if self.src.player_id == 0 else -ENV.in_row
        return self.obs.get(win_in, 0) > 0

    def is_op_win(self):
        op_state = ENV.op_win_state if self.src.player_id == 0 else -ENV.op_win_state
        return self.obs.get(op_state, 0) > 0


class F4State(AbState):

    @classmethod
    def new(cls, state, depth=None, player_id=None, **kw):
        if depth is None:
            ENV.set_mask(state)
            depth = len(ENV.pos_status[ENV.STATE_FIRST]) + len(
                ENV.pos_status[ENV.STATE_SECONED]
            )
            player_id = depth % 2
        return super().new(state, depth=depth, player_id=player_id, **kw)

    @classmethod
    def new_shape(cls, shape):
        ENV.set_shape(shape)
        return cls.new(ENV.INIT_MASK)

    def show_titles(self):
        return f"depth:{self.depth}, s:{ENV.s(self.player_id+1)} done:{self.done}"

    def get_action(self, pos):
        idx, state = ENV.get_next_state(self.state, pos, self.player_id)
        if state is None:
            return
        s = F4State.new(state, depth=self.depth + 1, player_id=1 - self.player_id)
        ENV.set_state(self.state)
        obs = ENV.get_move_obs(idx, 1 + self.player_id)
        return C4ACtion(self, pos, s, obs=obs)

    def make_actions(self):
        actions = []
        op_win_actions = []
        for pos in range(ENV.width):
            a = self.get_action(pos)
            if a is None:
                continue
            if a.get_dst().depth == ENV.size:
                a.dst.set_done(AbState.NO_WIN)
                return [a]
            if a.is_self_win():
                a.dst.set_done(
                    AbState.FIRST_WIN if self.player_id == 0 else AbState.SECONEND_WIN
                )
                return [a]
            if a.is_op_win():
                op_win_actions.append(a)
            else:
                actions.append(a)
        ret = op_win_actions if op_win_actions else actions
        return ret

    def to_str(self):
        return ENV.to_str(self.state)


class F4StateDev(F4State):
    pass
