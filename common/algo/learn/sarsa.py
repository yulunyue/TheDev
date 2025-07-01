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
        n_step=5,
        num_episodes=500,
    ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_step = n_step
        return super().load(use_cache, max_t, num_episodes)

    def take_action(self, state: State, **kw):
        if np.random.random() < self.epsilon:
            actions = list(state.get_actions().values())
            return actions[np.random.randint(len(actions))]
        return self.get_max_action(state)

    def get_max_action(self, state: State) -> Action:
        actions = list(state.get_actions().values())
        return actions[np.argmax([a.value for a in actions])]

    def search_main(self, state: State):
        self.rewards_record = []
        for _ in range(self.num_episodes):
            self.reward_tmp_all = 0
            self.run_one(state)
            self.rewards_record.append(self.reward_tmp_all)
            # logger.map(round=_, reward=self.reward_tmp_all)

    def run_one(self, state: State):
        raise Exception("todo")


class Sarsa(Base):
    def run_one(self, init_state: State, **kw):
        state: State = init_state.reset()
        action = self.take_action(state)
        self.actions: List[Action] = []
        while not action.dst.done:
            action = self.do_action(action)
            self.reward_tmp_all += action.reward
        init_state.set_best_action(self.take_action(init_state))

    def do_action(self, last_action: Action, **kw):
        next_state = last_action.dst
        action = self.take_action(next_state)
        self.update_2action(last_action, action)
        return action

    def update_2action(self, a0: Action, a1: Action):
        self.actions.append(a0)
        if len(self.actions) != self.n_step:
            return
        done = a0.dst.done
        g = a1.value
        for i in range(self.n_step - 1, -1, -1):
            s = self.actions[i]
            g = self.gamma * g + s.dst.reward
            if done and i > 0:
                s.value += self.alpha * (g - s.value)
        s = self.actions.pop(0)
        td_error = g - s.value
        s.value += self.alpha * td_error


class Qlearning(Base):
    def run_one(self, init_state: State, **kw):
        state: State = init_state.reset()
        action = self.take_action(state)
        while action:
            action = self.do_action(action)

        init_state.set_best_action(self.take_action(init_state))

    def do_action(self, a: Action):
        self.reward_tmp_all += a.reward
        self.update_action(a)
        if a.dst.done:
            return None
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
