from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger
from typing import List
import random


class Base(Algo):
    def load(
        self,
        alpha=0.1,
        gamma=0.9,
        epsilon=0.1,
        use_cache=False,
        max_t=-1,
        num_episodes=500,
    ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        return super().load(use_cache, max_t, num_episodes)

    def take_action(self, state: State, **kw):
        if state.done:
            return None
        if self.can_epsilon():
            actions = list(state.get_actions().values())
            return actions[np.random.randint(len(actions))]
        return self.get_max_action(state)

    def get_max_action(self, state: State) -> Action:
        actions = list(state.get_actions().values())
        return actions[np.argmax([a.value for a in actions])]

        # logger.map(round=_, reward=self.reward_tmp_all)

    def run_one(self, init_state: State):
        state: State = init_state
        while not state.done:
            action = self.take_action(state)
            self.reward_tmp_all += action.reward
            state = action.dst


class RandomEpisode(Base):
    def load(self, epsilon=1, **kw):
        return super().load(epsilon=epsilon, **kw)


class Sarsa(Base):
    def load(self, **kw):
        self.n_step = 1
        return super().load(**kw)

    def run_one(self, init_state: State, **kw):
        state: State = init_state
        action = self.take_action(state)
        self.actions: List[Action] = []
        while action:
            action = self.do_action(action)

    def do_action(self, action: Action, **kw):
        self.reward_tmp_all += action.reward
        next_action = self.take_action(action.dst)
        self.update_2action(action, next_action)
        if action.dst.done:
            return
        return next_action

    def update_2action(self, a0: Action, a1: Action):
        self.actions.append(a0)
        if len(self.actions) != self.n_step:
            return

        g = a1.value if a1 else 0
        done = a1 and a1.dst.done
        for i in range(len(self.actions) - 1, -1, -1):
            s = self.actions[i]
            g = s.reward + self.gamma * g
            # if done and i > 0:
            #     s.value += self.alpha * (g - s.value)
        s = self.actions.pop(0)
        td_error = g - s.value
        s.value += self.alpha * td_error
        if a0.src.state == 35:
            logger.debug(f"{a0.src}")


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


class Qlearning(Base):
    def run_one(self, init_state: State, **kw):
        state: State = init_state
        action = self.take_action(state)
        while action:
            action = self.do_action(action)

    def do_action(self, a: Action):
        self.reward_tmp_all += a.reward
        self.update_action(a)
        return self.take_action(a.dst)

    def q_learning(self, a0: Action):
        actions_value = [a.value for a in a0.dst.get_actions().values()]
        if actions_value:
            action_value = max(actions_value)
        else:
            action_value = 0
        td_error = a0.reward + self.gamma * action_value - a0.value
        a0.value += self.alpha * td_error

    def update_action(self, a0):
        self.q_learning(a0)


class DynaQ(Qlearning):
    def load(self, n_planning=0, **kw):
        self.n_planning = n_planning
        self.model = dict()
        return super().load(**kw)

    def update_action(self, a0: Action):
        self.q_learning(a0)
        self.model[(a0.src.state, a0.action)] = a0
        for _ in range(self.n_planning):
            s = random.choice(list(self.model.values()))
            self.q_learning(s)
