from common.algo.export import AbState, Action
from common.util.export import List
from .constant import C, CS


class C5ACtion(Action):
    def __init__(self, src, action, dst, obs):
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

    def is_self_win(self):  # 自己能赢
        win_in = C.in_row if self.src.player_id == 0 else -C.in_row
        return self.obs.get(win_in, 0) > 0

    def is_op_win(self):  # 不走对手能赢
        op_state = C.op_win_state if self.src.player_id == 0 else -C.op_win_state
        return self.obs.get(op_state, 0) > 0


class State(AbState):

    def __init__(self, state, player_id=None, depth=None):
        if depth is None:
            C.set_state(state)
            self.done, player_id, depth = C.game_over()
        super().__init__(state, player_id=player_id, depth=depth)

    def get_action_by_pos(self, pos):
        C.set_state(self.state)
        obs, state = C.get_next_state(pos, self.player_id + 1)
        dst = State.new(state, player_id=1 - self.player_id, depth=self.depth + 1)
        a = C5ACtion(self, pos, dst, obs=obs)
        return a

    def get_win_player(self, *args, **kw):
        return self.done - 1

    def make_actions(self):
        actions = []
        actions_op_win = []
        C.set_state(self.state)  # 在深度搜索需要确保
        can_moves = list(C.pos_status[C.STATE_NULL])
        for pos in can_moves:
            a = self.get_action_by_pos(pos)
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
        if len(actions_op_win) > 1:
            self.set_done(
                AbState.FIRST_WIN if self.player_id == 0 else AbState.SECONEND_WIN
            )
        return actions_op_win if actions_op_win else actions

    def to_str(self):
        return CS.set_state(self.state).to_str()

    def show_titles(self):
        return f"depth:{self.depth}; player:{self.player_id}{C.s(self.player_id+1)}; done:{self.done}"
