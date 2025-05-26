from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log

logger = get_log("ln", fmt="")


class Sarsa(Algo):
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
        actions = list(state.get_actions().values())
        if np.random.random() < self.epsilon and 0:
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

        return reward

    def run(self, state_cls: State):
        rewards = []
        for _ in range(self.num_episodes):
            rewards.append(self.run_one(state_cls))
        return rewards

    def update(self, a0: Action, a1: Action):
        r = a1.dst.reward
        td_error = r + self.gamma * a1.value - a0.value
        a0.value += self.alpha * td_error
        max_value = max([v.value for v in a0.src.get_actions().values()])
        a0.p = 1 if max_value == a0.value else 0
        logger.info(
            f"s0:{a0.dst.state}, a0:{a0.action}, r:{r}, s1:{a1.dst.state}, a1:{a1.action}, q0:{a0.value}, q1:{a1.value}"
        )
