from common.algo.export import AbState, Action
from common.util.export import List, Dict
import random


class TestState(AbState):
    idx = 0

    def game_over(self):
        if not self.get_sort_actions():
            return True
        return super().game_over()

    def get_current_player(self):
        return self.player_id

    @property
    def availables(self):
        return self.get_sort_actions()

    @classmethod
    def get_new_id(cls):
        cls.idx += 1
        return cls.idx

    @classmethod
    def make_random_state(cls, size=40, min_v=2, max_v=6):
        s = TestState.new().set_player_id(0)
        q = [s]
        while len(q) < size:
            idx = random.randint(0, len(q) - 1)
            cur_state = q.pop(idx)
            states = []
            for i in range(random.randint(min_v, max_v)):
                states.append(TestState.new())
                q.append(states[-1])
            cur_state.set_next_states(states)
        random.shuffle(q)
        for i, v in enumerate(q):
            v.set_reward(i - len(q) // 2)
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
        if player_id is not None:
            ret.set_player_id(player_id)
        ret.money = r
        ret.set_next_states(states or [])
        return ret

    def set_next_states(self, states: List["TestState"]):
        return self.set_actions(
            [
                Action(self, i, v.set_player_id(1 - self.player_id))
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
                r=4,
            ),
            cls.make(
                cls.make(r=3),
                cls.make(r=-9),
                cls.make(r=-3),
                r=-3,
            ),
            player_id=1,
        )

    def show_titles(self):
        if self.game_over:
            return f"r:{self.money}"
        return f"p:{self.player_id}; r:{self.money}"

    @classmethod
    def get_root(cls):
        return cls.make_test_state()
