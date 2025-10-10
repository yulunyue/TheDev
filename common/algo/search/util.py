from .state import MctsState, Action, AbState, State
import random


class TestState(AbState):
    idx = 0

    @staticmethod
    def get_new_id():
        TestState.idx += 1
        return TestState.idx

    @staticmethod
    def make_random_state(width=3, height=3):
        random.seed(3)

        def util(w, h, reward):
            ret = TestState.new(TestState.idx).set_reward(reward)
            ret.player_id = h % 2
            TestState.idx += 1
            if h == height:
                ret.set_done(True)
                return ret
            ret.actions = []
            for i in range(w):
                r = random.randint(0, 10)
                dst = util(w, h + 1, reward + (r if h % 2 == 0 else -r))
                ret.actions[i] = Action(ret, "", dst).set_reward(r)
            return ret

        return util(width, 0, 0)

    max_reward = None

    @classmethod
    def new(cls, *states, r=None, max_reward=None, player_id=None):
        ret: TestState = super().new(TestState.get_new_id()).set_reward(r)
        if player_id is not None:
            ret.set_player_id(player_id)
        ret.max_reward = r if max_reward is None else max_reward
        ret.set_next_states(states or [])
        ret.init_data()

        return ret

    @staticmethod
    def make_test_state():
        return TestState.new(
            TestState.new(r=1),
            TestState.new(
                TestState.new(r=0),
                TestState.new(r=-5),
            ),
            TestState.new(
                TestState.new(r=1),
                TestState.new(r=-9),  # 不会选这个
            ),
            player_id=1,
        )

    def get_done(self):
        if self.get_sort_actions():
            return
        if self.get_reward() == 0:
            return 2
        return 0 if self.get_reward() > 0 else 1
