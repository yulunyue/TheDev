from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List
from common.algo.learn.base import Base


class MctsEasy(Base):
    def run_one(self, init_state: State, **kw):
        state = init_state
        actions: List[Action] = []
        while not state.done:
            action = self.take_action(state)
            actions.append(action)
            self.reward_tmp_all += action.reward
            state = action.dst
        vt = set()
        g = 0
        while actions:
            a = actions.pop()
            k = a.src.state, a.action
            g = self.gamma * g + a.reward
            if k not in vt:
                vt.add(k)
                a.visite_num += 1
                a.value += (g - a.value) / a.visite_num
