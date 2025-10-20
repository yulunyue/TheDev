from .state import Action, AbState, State
from common.util.export import random, List


class TestState(AbState):
    idx = 0

    def game_end(self):
        if not self.get_sort_actions():
            return True, self.get_done()
        if self.get_done() is not None:
            return True, self.get_done()
        return False, None

    def get_current_player(self):
        return self.player_id

    @property
    def availables(self):
        return self.get_sort_actions()

    @staticmethod
    def get_new_id():
        TestState.idx += 1
        return TestState.idx

    @staticmethod
    def make_random_state(size=40, min_v=2, max_v=6):
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

    def set_reward(self, r):
        if r == 0:
            self.set_done(2)
        elif isinstance(r, int) and r < 0:
            self.set_done(0)
        elif isinstance(r, int) and r > 0:
            self.set_done(1)
        return super().set_reward(r)

    @classmethod
    def new(cls, *states, r=None, player_id=None):
        ret: TestState = super().new(TestState.get_new_id())
        if player_id is not None:
            ret.set_player_id(player_id)
        if r is not None:
            ret.set_reward(r)
        ret.set_next_states(states or [])
        ret.init_data()
        return ret

    @staticmethod
    def make_test_state():
        return TestState.new(
            TestState.new(r=1),
            TestState.new(
                TestState.new(r=2),
                TestState.new(r=-5),
            ),
            TestState.new(
                TestState.new(r=3),
                TestState.new(r=-9),  # 不会选这个
                TestState.new(r=-3),  # 不会选这个
            ),
            player_id=1,
        )

    def get_done(self):
        if self.get_sort_actions():
            return
        if self.get_reward() == 0:
            return 2
        return 0 if self.get_reward() > 0 else 1
