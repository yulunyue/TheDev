from common.algo.export import AbState, Action
from common.util.export import List, Dict, logger
import random


class TestAction(Action):
    def get_reward(self, **kwargs):
        d: TestState = self.get_dst()
        d.vt = True
        return d.money if self.src.player_id == 0 else -d.money

    def do(self):
        d: TestState = self.get_dst()
        return super().do()


class TestState(AbState):
    idx = 0
    vt = False

    def game_over(self):
        if not self.get_sort_actions():
            return True
        return super().game_over()

    def get_current_player(self):
        return self.player_id

    def reset(self):
        def util(s: TestState, *args):
            s.vt = False

        self.dfs(util)
        return self

    @property
    def availables(self):
        return self.get_sort_actions()

    @classmethod
    def get_new_id(cls):
        cls.idx += 1
        return cls.idx

    @classmethod
    def new_random_state(cls, size=20, min_v=2, max_v=6):
        s = TestState.new().set_player_id(0)
        q = [s]
        while len(q) < size:
            idx = random.randint(0, len(q) - 1)
            cur_state: TestState = q.pop(idx)
            states = []
            for i in range(random.randint(min_v, max_v)):
                states.append(TestState.make(r=None))
                q.append(states[-1])
            cur_state.set_next_states(states)

        return s

    @classmethod
    def new(cls, state=None, **kw):
        if state is None:
            state = TestState.get_new_id()
        return super().new(state, **kw)

    money = 0

    @classmethod
    def make(cls, *states, r=0, player_id=None):

        ret: TestState = cls.new()
        if r is None:
            r = random.randint(-10, 10)
        if player_id is not None:
            ret.set_player_id(player_id)
        ret.money = r
        ret.set_next_states(states or [])
        return ret

    def set_next_states(self, states: List["TestState"]):
        return self.set_actions(
            [
                TestAction(self, i, v.set_player_id(1 - self.player_id))
                for i, v in enumerate(states)
            ]
        )

    @classmethod
    def make_test_state(cls):
        return cls.make(
            cls.make(r=1),
            cls.make(
                cls.make(r=2),
                cls.make(r=-5),
            ),
            cls.make(
                cls.make(r=3),
                cls.make(r=-9),
                cls.make(r=-3),
            ),
            player_id=1,
        )

    def show_titles(self):
        if self.game_over():
            ans = f"s:{self.state}; r:{self.money}"
            if self.vt:
                ans += " *"
        else:
            ans = f"s:{self.state}; p:{self.player_id}"
            if hasattr(self, "alpha"):
                alpha = self.alpha if self.player_id == 0 else -self.alpha
                ans += f"; alpha:{alpha}"
        if self.extra:
            ans += f"; vt={self.extra.n_visits}; qv={'%.3f'%self.extra.q}; uv={'%.3f'%self.extra.u}"
        return ans

    @classmethod
    def get_root(cls):
        return cls.make_test_state()
