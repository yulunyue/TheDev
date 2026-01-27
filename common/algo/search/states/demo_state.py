from .state import Action
from .mctsstate import MctsState
from common.util.export import List, Dict, logger, random, uid
from .demo_action import DemoAction


class DemoState(MctsState):

    def game_over(self):
        return self.done

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
    def make(cls, *states, r=None, player_id=None):
        ret: DemoState = cls("")
        ret.r = r
        if player_id is None:
            player_id = 0
        ret.actions = []
        for i, s in enumerate(states):
            a = DemoAction(ret, i, s)
            ret.actions.append(a)
        return ret.set_player_id(player_id).set_done(len(ret.actions) == 0)

    def get_children(self):
        return [v for v in super().get_children() if v.src.has_visited]

    @classmethod
    def make_test_state(cls):
        return cls.make(
            cls.make(r=1),
            cls.make(
                cls.make(r=1),
                cls.make(r=0),
            ),
            cls.make(
                cls.make(r=0),
                cls.make(r=1),
                cls.make(r=0),
            ),
            player_id=1,
        )
