from ..learn.sarse.mctssearch import MctsState, Action
import random


class TestState(MctsState):

    @staticmethod
    def make_test_state(width=3, height=3):
        random.seed(3)
        TestState.idx = 0

        def util(w, h, reward):
            ret = TestState.new(TestState.idx).set_reward(reward)
            ret.player_id = h % 2
            TestState.idx += 1
            if h == height:
                ret.set_done(True)
                return ret
            ret.actions = dict()
            for i in range(w):
                r = random.randint(0, 10)
                dst = util(w, h + 1, reward + (r if h % 2 == 0 else -r))
                ret.actions[i] = Action(ret, i, dst).set_reward(r)
            return ret

        return util(width, 0, 0)
