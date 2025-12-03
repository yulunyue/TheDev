from common.algo.export import AbState, Action
from common.util.export import List
from .constant import C

C.load()


class C5ACtion(Action):
    def __init__(self, src, action, dst=None, obs=None):
        super().__init__(src, action, dst)
        self.set_obs(obs)

    def set_obs(self, obs):
        self.obs: dict = obs
        r = 0
        if self.is_self_win():
            r = 1
        self.set_reward(r)

    def show(self):
        y, x = self.action // C.width, self.action % C.width
        return f"src:{self.src.state}, dst:{self.dst.state}, action:{y},{x},{C.s(self.src.player_id+1)}, obs:{self.obs} r:{self.get_reward()}"

    def is_self_win(self):
        win_in = C.in_row if self.src.player_id == 0 else -C.in_row
        return self.obs.get(win_in, 0) > 0

    def is_op_win(self):
        op_state = C.op_win_state if self.src.player_id == 0 else -C.op_win_state
        return self.obs.get(op_state, 0) > 0


class State(AbState):
    @classmethod
    def new(cls, state=None, player_id=None, depth=None) -> "State":
        if state is None:
            state = C.state
        if depth is None:
            C.set_mask(state)
            depth = len(C.pos_status[C.STATE_FIRST]) + len(
                C.pos_status[C.STATE_SECONED]
            )
            player_id = depth % 2
        return super().new(state, player_id=player_id, depth=depth)

    def get_action(self, pos):
        C.set_mask(self.state)
        obs, state = C.get_next_state(pos, self.player_id + 1)
        dst = State.new(state, player_id=1 - self.player_id, depth=self.depth + 1)
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
        return C.to_str(self.state)

    def show_titles(self):
        return f"depath:{self.depth}; player:{self.player_id}{C.s(self.player_id+1)}"
