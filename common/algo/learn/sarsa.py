from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log
from typing import List

logger = get_log("ln", fmt="")


class Sarsa(Algo):
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
        actions = list(state.get_actions().values())
        if np.random.random() < self.epsilon:
            action = np.random.randint(len(actions))
        else:
            action = np.argmax([a.value for a in actions])
        return actions[action]

    def run_one(self, state_cls: State, **kw):
        state: State = state_cls.get_init_state()
        last_action = self.take_action(state)
        reward = 0
        while not state.done:
            state = last_action.dst
            action = self.take_action(state)
            reward += action.dst.reward
            self.update(last_action, action)
            last_action = action
        self.actions.clear()
        return reward

    def run(self, state_cls: State):
        rewards = []
        self.actions: List[Action] = []
        for _ in range(self.num_episodes):
            rewards.append(self.run_one(state_cls))
        return rewards

    def update(self, a0: Action, a1: Action):
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
        # a0.value += self.alpha * td_error


class Qlearning(Sarsa):
    def run_one(self, state_cls: State, **kw):
        state: State = state_cls.get_init_state()
        reward = 0
        while not state.done:
            a = self.take_action(state)
            reward += a.dst.reward
            self.update(a)
            state = a.dst
        return reward

    def update(self, a0: Action):
        action = [a.value for a in a0.dst.get_actions().values()]
        td_error = a0.dst.reward + self.gamma * max(action) - a0.value
        a0.value += self.alpha * td_error
