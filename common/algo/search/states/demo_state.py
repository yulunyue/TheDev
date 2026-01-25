from .state import Action
from .mctsstate import MctsState
from common.util.export import List, Dict, logger, random, uid
from .demo_action import DemoAction


class DemoState(MctsState):

    def game_over(self):
        return False if self.actions else True

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

    r = None

    @classmethod
    def make(cls, *states, r=0, player_id=None):
        ret: DemoState = cls("")
        ret.r = r
        if player_id is None:
            player_id = 0
        actions = []
        for i, s in enumerate(states):
            a = DemoAction(ret, i).set_next_state(s)
            actions.append(a)

        return ret.set_player_id(player_id).set_actions(actions)

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
